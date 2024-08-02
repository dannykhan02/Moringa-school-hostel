from dotenv import load_dotenv
import os


load_dotenv()


stripe_secret_key = os.getenv('STRIPE_TEST_SECRET_KEY')

if stripe_secret_key:
    print(f"STRIPE_TEST_SECRET_KEY is loaded: {stripe_secret_key}")
else:
    print("STRIPE_TEST_SECRET_KEY is not set. Please check your .env file.")
