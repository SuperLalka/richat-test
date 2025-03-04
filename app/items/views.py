import json
import logging
from urllib.request import Request

from django.conf import settings
from django.db.models import Case, When, Value

from django.http import HttpResponse, JsonResponse
from django.views import generic
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView

from app.items.models import Item, PaymentSession, Order
from app.utils.handlers import StripeWebhooksHandler
from app.utils.stripe import stripe_client

logger = logging.getLogger('django')


class HomePageView(TemplateView):
    template_name = "base.html"


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
            .prefetch_related('prices', 'prices__currency')
        )
        return context


class OrdersListPageView(generic.ListView):
    model = Order
    template_name = "pages/orders.html"

    def get_context_data(self, **kwargs):
        context = super(OrdersListPageView, self).get_context_data(**kwargs)
        context['orders'] = (
            Order.objects.all()
            .prefetch_related('items', 'discounts', 'taxes')
            .select_related('pay_session')
        )
        return context


def buy(request: Request):
    data = json.loads(request.body)
    currency = request.COOKIES.get('currency', settings.DEFAULT_CURRENCY)

    items = Item.objects.filter(id__in=[int(item_id) for item_id in data['items_ids']])
    line_items = [
        {
            'price_data': {
                'currency': currency,
                'product_data': {
                    'name': item.name,
                },
                'unit_amount': item.prices.get(currency__name_iso=currency).unit_amount,
            },
            'quantity': 1,
        } for item in items
    ]

    session = stripe_client.checkout.Session.create(
        line_items=line_items,
        mode='payment',
        success_url=f'{settings.SITE_URL}/buy/success/',
        cancel_url=f'{settings.SITE_URL}/buy/cancel/',
    )
    PaymentSession.objects.create(session_id=session.id, user_id=settings.TEST_USER_ID)
    return JsonResponse({'session_url': session.url}, status=200)


@require_http_methods(['POST'])
def webhooks(request: Request):
    try:
        event_obj = json.loads(request.body)
    except Exception:
        return HttpResponse(400)

    webhook_handler = StripeWebhooksHandler(event_obj)

    logger.info("Received webhook with content \n %s", event_obj)

    if event_obj['type'] == 'checkout.session.completed':
        webhook_handler.complete_checkout_session()
    else:
        logger.warning('Unhandled event type {}'.format(event_obj.get('type')))

    return HttpResponse(200)
