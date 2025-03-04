from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Item(models.Model):
    name = models.CharField()
    description = models.TextField(blank=True, null=True)

    stripe_obj_id = models.CharField(default='')

    class Meta:
        db_table = 'item'
        verbose_name = _('Item')
        verbose_name_plural = _('Items')

    def __str__(self):
        return self.name


class Currency(models.Model):
    name_iso = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=30, blank=True, default='')
    symbol = models.CharField(max_length=10, blank=True, default='')

    class Meta:
        db_table = 'currency'
        verbose_name = _('Currency')
        verbose_name_plural = _('Currencies')

    def __str__(self):
        return self.name_iso


class Price(models.Model):
    unit_amount = models.IntegerField(null=True, blank=True, default=None)

    stripe_obj_id = models.CharField(default='')

    currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        related_name='prices',
    )
    product = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name='prices',
    )

    class Meta:
        db_table = 'price'
        verbose_name = _('Price')
        verbose_name_plural = _('Prices')

    def __str__(self):
        return self.stripe_obj_id

    def humanize_unit_amount(self):
        return '{:.2f}'.format(self.unit_amount/100)


class PaymentSession(models.Model):
    session_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='pay_sessions',
    )
    order = models.OneToOneField(
        'Order',
        on_delete=models.CASCADE,
        related_name='pay_session',
        blank=True,
        null=True
    )

    class Meta:
        db_table = 'payment_session'
        verbose_name = _('PaymentSession')
        verbose_name_plural = _('PaymentSessions')


class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders',
    )

    items = models.ManyToManyField(
        Item,
    )
    discounts = models.ManyToManyField(
        'Discount',
        blank=True,
    )
    taxes = models.ManyToManyField(
        'Tax',
        blank=True,
    )

    class Meta:
        db_table = 'order'
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')


class Discount(models.Model):
    name = models.CharField()
    value = models.CharField()

    class Meta:
        db_table = 'discount'
        verbose_name = _('Discount')
        verbose_name_plural = _('Discounts')


class Tax(models.Model):
    name = models.CharField()
    value = models.CharField()

    class Meta:
        db_table = 'tax'
        verbose_name = _('Tax')
        verbose_name_plural = _('Taxes')
