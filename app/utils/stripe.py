import os

import stripe as stripe_client

stripe_client.api_key = os.getenv('STRIPE_SECRET_KEY')
