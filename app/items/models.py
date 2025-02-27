from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Item(models.Model):
    name = models.CharField()
    description = models.TextField(blank=True, null=True)

    stripe_obj_id = models.CharField(default='')

    # currency =

    class Meta:
        db_table = 'item'
        verbose_name = _('Item')
        verbose_name_plural = _('Items')

    def __str__(self):
        return self.name


class Price(models.Model):
    currency = models.CharField()
    unit_amount = models.IntegerField(null=True, blank=True, default=None)

    stripe_obj_id = models.CharField(default='')

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
