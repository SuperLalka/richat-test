import json
from urllib.request import Request

from django.db.models import Case, When, Value

from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.views import generic
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView

from app.items.models import Item
from app.utils.stripe import stripe_client


class HomePageView(TemplateView):
    template_name = "base.html"

    def get_context_data(self, **kwargs):
        # kwargs['users'] = User.objects.all()
        return super(HomePageView, self).get_context_data(**kwargs)


class ItemDetailPageView(generic.DetailView):
    model = Item
    template_name = None


class ItemListPageView(generic.ListView):
    model = Item
    template_name = "pages/items.html"

    def get_context_data(self, **kwargs):
        context = super(ItemListPageView, self).get_context_data(**kwargs)
        context['items'] = (
            Item.objects.all()
                .annotate(in_basket=Case(
                    When(baskets__isnull=True, then=Value(False)), default=Value(True)
                ))
                .prefetch_related('prices')
        )
        return context


def buy(request: Request):
    data = json.loads(request.body)

    items = Item.objects.filter(id__in=[int(item_id) for item_id in data['items_ids']])
    line_items = [
        {
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': item.name,
                },
                'unit_amount': item.prices.first().unit_amount,
            },
            'quantity': 1,
        } for item in items
    ]

    session = stripe_client.checkout.Session.create(
        line_items=line_items,
        mode='payment',
        success_url='http://localhost:8000/buy/success/',
        cancel_url='http://localhost:8000/buy/cancel/',
    )
    return JsonResponse({'session_url': session.url}, status=200)


@require_http_methods(['POST'])
def webhooks(request: Request):
    payload = request.data

    try:
        event = json.loads(payload)
    except json.decoder.JSONDecodeError as e:
        print('Webhook error while parsing basic request.' + str(e))
        return HttpResponse(400)

    if event and event['type'] == 'checkout.session.completed':
        payment_intent = event['data']['object']
        print('Payment for {} succeeded'.format(payment_intent['amount']))
        print(event)
    else:
        # Unexpected event type
        print('Unhandled event type {}'.format(event['type']))

    return HttpResponse(200)
