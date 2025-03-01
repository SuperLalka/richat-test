
from background_task import background
from django.contrib.auth import get_user_model

from app.utils.stripe import stripe_client
from app.items.utils import sync_product_with_stripe

User = get_user_model()


def sync_products_with_stripe():
    @background()
    def sync_single_product(stripe_product: dict):
        sync_product_with_stripe(stripe_product)

    for product in stripe_client.Product.list().data:
        sync_single_product.now({
            'id': product.id,
            'name': product.name,
            'description': product.description
        })
