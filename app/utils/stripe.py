import os

import stripe as stripe_client

stripe_client.api_key = os.getenv('STRIPE_SECRET_KEY')

# starter_subscription = stripe.Product.create(
#   name="Starter Subscription",
#   description="$12/Month subscription",
# )
#
# starter_subscription_price = stripe.Price.create(
#   unit_amount=1200,
#   currency="usd",
#   recurring={"interval": "month"},
#   product=starter_subscription['id'],
# )
