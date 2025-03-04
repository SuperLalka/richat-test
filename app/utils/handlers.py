import datetime

from django.db import transaction

from app.items.models import Order, PaymentSession


class StripeWebhooksHandler:
    def __init__(self, event_obj: dict = None):
        self.event_obj = event_obj

    def complete_checkout_session(self) -> None:
        with transaction.atomic():
            session = PaymentSession.objects \
                .filter(session_id=self.event_obj['id']) \
                .select_related('user', 'user__userbasket') \
                .first()

            basket = session.user.userbasket
            order = Order.objects.create(user=session.user)
            order.items.add(*list(basket.items.values_list('id', flat=True)))
            basket.items.clear()

            session.completed_at = datetime.datetime.now()
            session.order = order
            session.save(update_fields=['completed_at', 'order'])
