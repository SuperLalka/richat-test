from urllib.request import Request

from django.db.models import Sum
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView

from app.users.models import UserBasket


class BasketPageView(TemplateView):
    template_name = 'pages/basket.html'

    def get_context_data(self, **kwargs):
        kwargs['basket'] = (
            UserBasket.objects.all()
            .annotate(total_price=Sum('items__prices__unit_amount'))
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
