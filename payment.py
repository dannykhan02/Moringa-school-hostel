from flask_restful import Resource
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import stripe
import os
from dotenv import load_dotenv

load_dotenv()

stripe.api_key = os.getenv('STRIPE_TEST_SECRET_KEY')

class PaymentResource(Resource):
    @jwt_required()
    def post(self):
        try:
            data = request.json
            token = data['tokenId']
            amount = data['amount']
            currency = data['currency']

            charge = stripe.Charge.create(
                amount=amount,  
                currency=currency,  
                description='Example charge',
                source=token
            )

            return jsonify({'success': True, 'charge_id': charge.id})

        except stripe.error.CardError as e:
            return jsonify({'success': False, 'error': str(e)})

class VerifyPaymentResource(Resource):
    @jwt_required()
    def get(self, charge_id):
        try:
            
            charge = stripe.Charge.retrieve(charge_id)
            return jsonify(charge)
        except stripe.error.StripeError as e:
            return jsonify({'error': str(e)}), 400
