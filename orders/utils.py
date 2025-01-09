# utils.py
import requests
import base64
from datetime import datetime
from django.conf import settings
import json

def generate_access_token():
    consumer_key = settings.MPESA_CONSUMER_KEY
    consumer_secret = settings.MPESA_CONSUMER_SECRET
    auth = base64.b64encode(f"{consumer_key}:{consumer_secret}".encode()).decode()
    
    try:
        res = requests.get(
            'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials',
            headers={'Authorization': f'Basic {auth}'}
        )
        return res.json()['access_token']
    except Exception as e:
        print(f"Access token generation error: {str(e)}")
        return None

def generate_password():
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    shortcode = settings.MPESA_SHORTCODE
    passkey = settings.MPESA_PASSKEY
    
    password_str = f"{shortcode}{passkey}{timestamp}"
    return base64.b64encode(password_str.encode()).decode(), timestamp

def lipa_na_mpesa_online(phone_number, amount, reference, description):
    access_token = generate_access_token()
    if not access_token:
        return {'ResponseCode': '1', 'ResponseDescription': 'Could not generate access token'}
    
    password, timestamp = generate_password()
    
    # Ensure amount is an integer
    amount = int(float(amount))
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }
    
    payload = {
        "BusinessShortCode": settings.MPESA_SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": settings.MPESA_SHORTCODE,
        "PhoneNumber": phone_number,
        "CallBackURL": settings.MPESA_CALLBACK_URL,
        "AccountReference": reference,
        "TransactionDesc": description
    }
    
    try:
        api_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
        response = requests.post(api_url, json=payload, headers=headers)
        
        # Print debugging information
        print(f"Request payload: {payload}")
        print(f"Response: {response.text}")
        
        return response.json()
    except Exception as e:
        print(f"API request error: {str(e)}")
        return {'ResponseCode': '1', 'ResponseDescription': str(e)}