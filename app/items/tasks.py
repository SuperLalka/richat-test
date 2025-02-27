
from celery import group
from django.contrib.auth import get_user_model

from app.utils.stripe import stripe_client
from app.items.utils import sync_product_with_stripe
from config.celery_app import app

User = get_user_model()


@app.task
def sync_products_with_stripe():
    group([
        sync_single_product.s({
            'id': product.id,
            'name': product.name,
            'description': product.description
        }) for product in stripe_client.Product.list().data
    ])()


@app.task
def sync_single_product(stripe_product: dict):
    sync_product_with_stripe(stripe_product)
