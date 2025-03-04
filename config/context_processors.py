from django.conf import settings

from app.items.models import Currency


def currencies(request):
    return {
        'currencies': Currency.objects.all(),
        'currently_currency': request.COOKIES.get('currency', settings.DEFAULT_CURRENCY)
    }
