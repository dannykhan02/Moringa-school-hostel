import stripe
import os
from dotenv import load_dotenv

load_dotenv() 

stripe.api_key = os.getenv('STRIPE_TEST_SECRET_KEY')

if not stripe.api_key:
    raise ValueError("Stripe API key not found. Please set it in the .env file.")


token_id = "tok_visa"

try:
    charge = stripe.Charge.create(
        amount=5000,  
        currency='usd',
        description='Test charge',
        source=token_id
    )
    print(f"Charge successful: {charge.id}")
except stripe.error.CardError as e:
    print(f"Card Error: {e}")
except stripe.error.StripeError as e:
    print(f"Stripe Error: {e}")
