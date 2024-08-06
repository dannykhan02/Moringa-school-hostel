import requests
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from datetime import datetime
from requests.auth import HTTPBasicAuth
import base64

app = Flask(__name__)
api = Api(app)


MPESA_CONSUMER_KEY = 'AvnO2hFOvgnTjC3DhjjsPvSZg43wx2pKR7mppwnEpXcofgXq'
MPESA_CONSUMER_SECRET = '79BL7sZjAfsK6ffS7NzgOpnglJhS11Vh2FAaxleIZRkaKXMfQ2l9qbk0R39CuOrD'
MPESA_BUSINESS_SHORT_CODE = '174379'
MPESA_PASSKEY = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
MPESA_CALLBACK_URL = 'https://mydomain.com/path'
MPESA_ACCOUNT_REFERENCE = 'Moringa Hostel'
MPESA_TRANSACTION_DESC = 'Payment for Moringa Hostel'

def get_mpesa_access_token():
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(url, auth=HTTPBasicAuth(MPESA_CONSUMER_KEY, MPESA_CONSUMER_SECRET))
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        raise Exception("Failed to fetch access token")

def generate_password(business_short_code, passkey, timestamp):
    data_to_encode = business_short_code + passkey + timestamp
    encoded_string = base64.b64encode(data_to_encode.encode())
    return encoded_string.decode('utf-8')

class MpesaPaymentResource(Resource):
    def post(self):
        try:
            data = request.json
            amount = data.get('amount')
            phone_number = data.get('phone_number')

            if not amount or not phone_number:
                return jsonify({'success': False, 'error': 'Amount and phone number are required'})

            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            password = generate_password(MPESA_BUSINESS_SHORT_CODE, MPESA_PASSKEY, timestamp)
            
            payload = {
                "BusinessShortCode": MPESA_BUSINESS_SHORT_CODE,
                "Password": password,
                "Timestamp": timestamp,
                "TransactionType": "CustomerPayBillOnline",
                "Amount": str(amount),  
                "PartyA": str(phone_number),  
                "PartyB": MPESA_BUSINESS_SHORT_CODE,
                "PhoneNumber": str(phone_number), 
                "CallBackURL": MPESA_CALLBACK_URL,
                "AccountReference": MPESA_ACCOUNT_REFERENCE,
                "TransactionDesc": MPESA_TRANSACTION_DESC
            }

            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {get_mpesa_access_token()}'
            }

            response = requests.post('https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest', json=payload, headers=headers)

            if response.status_code == 200:
                return jsonify({'success': True, 'response': response.json()})
            else:
                return jsonify({'success': False, 'error': response.text})

        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})

class MpesaCallbackResource(Resource):
    def post(self):
        data = request.json
        print(data)
        return jsonify({'success': True})


api.add_resource(MpesaPaymentResource, '/mpesa_payment')
api.add_resource(MpesaCallbackResource, '/mpesa_callback')

if __name__ == '__main__':
    app.run(debug=True)
