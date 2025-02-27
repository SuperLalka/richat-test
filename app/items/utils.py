
from app.items.models import Item, Price
from app.utils.stripe import stripe_client


def sync_product_with_stripe(stripe_product: dict):
    defaults = {
        'name': stripe_product['name'],
        'description': stripe_product['description']
    }
    product, _ = Item.objects.update_or_create(
        stripe_obj_id=stripe_product['id'],
        defaults=defaults,
        create_defaults=defaults
    )

    for price in stripe_client.Price.list(product=stripe_product["id"], active=True):
        defaults = {
            'currency': price['currency'],
            'unit_amount': price['unit_amount'],
        }
        Price.objects.update_or_create(
            stripe_obj_id=price['id'],
            product=product,
            defaults=defaults,
            create_defaults=defaults
        )
