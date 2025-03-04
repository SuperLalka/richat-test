from urllib.request import Request

from django.conf import settings
from django.db.models import Func, IntegerField, Value, F, FloatField
from django.db.models.functions import Coalesce, Cast
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView

from app.items.models import Price
from app.users.models import UserBasket


class BasketPageView(TemplateView):
    template_name = 'pages/basket.html'

    def get_context_data(self, **kwargs):
        currency = self.request.COOKIES.get('currency', settings.DEFAULT_CURRENCY)

        user_basket = UserBasket.objects.all()
        basket_items = user_basket.first().items

        tp_subquery = Price.objects \
            .filter(currency=currency, product__in=basket_items.all()) \
            .annotate(total_price=Coalesce(
                Func('unit_amount', function='Sum'), Value(0), output_field=IntegerField()
            )) \
            .values('total_price')

        kwargs['basket'] = (
            user_basket
            .annotate(total_price=tp_subquery)
            .annotate(humanize_total_price=Cast(F('total_price') / 100.0, output_field=FloatField()))
            .prefetch_related('items', 'items__prices')
            .first()
        )
        return super(BasketPageView, self).get_context_data(**kwargs)


@require_http_methods(['POST', 'DELETE'])
def operation(request: Request, item_id: int):
    item_in = item_id in UserBasket.objects.first().items.all().values_list('id', flat=True)

    if request.method == 'POST':
        if item_in:
            return HttpResponse(status=400)

        UserBasket.objects.first().items.add(item_id)
        return HttpResponse(status=201)
    else:  # 'DELETE'
        if not item_in:
            return HttpResponse(status=400)

        UserBasket.objects.first().items.remove(item_id)
        return HttpResponse(status=204)
