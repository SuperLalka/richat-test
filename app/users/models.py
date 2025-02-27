
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from app.users.managers import UserManager


class User(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_absolute_url(self) -> str:
        return reverse('users:detail', kwargs={'pk': self.id})


class UserBasket(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    items = models.ManyToManyField(
        'items.Item',
        blank=True,
        related_name='baskets',
    )

    class Meta:
        db_table = 'user_basket'
        verbose_name = _('UserBasket')
        verbose_name_plural = _('UserBaskets')

    def __str__(self):
        return f"Basket {self.user.email}"
