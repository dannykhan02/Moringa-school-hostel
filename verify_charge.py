import stripe
import os
from dotenv import load_dotenv


load_dotenv()


stripe.api_key = os.getenv('STRIPE_TEST_SECRET_KEY')

def verify_charge(charge_id):
    try:
       
        charge = stripe.Charge.retrieve(charge_id)
        return charge
    except stripe.error.StripeError as e:
        
        return {'error': str(e)}


charge_id = "ch_3PjEH0KEK9WG68Q61IKvcVlN"  
charge_details = verify_charge(charge_id)

print("Charge details:", charge_details)
