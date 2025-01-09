import requests
from django.conf import settings
from datetime import datetime
import base64
import logging

logger = logging.getLogger(__name__)

def get_mpesa_access_token():
    consumer_key = settings.MPESA_CONSUMER_KEY
    consumer_secret = settings.MPESA_CONSUMER_SECRET
    api_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials' if settings.MPESA_ENV == 'sandbox' else 'https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    response = requests.get(api_url, auth=(consumer_key, consumer_secret))
    access_token = response.json().get('access_token')
    
    if not access_token:
        logger.error("Failed to get M-Pesa access token: %s", response.text)

    return access_token

def lipa_na_mpesa_online(phone_number, amount, account_reference, transaction_desc):
    access_token = get_mpesa_access_token()
    api_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest' if settings.MPESA_ENV == 'sandbox' else 'https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest'

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    password = base64.b64encode(f"{settings.MPESA_SHORTCODE}{settings.MPESA_PASSKEY}{timestamp}".encode()).decode('utf-8')

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
        "AccountReference": account_reference,
        "TransactionDesc": transaction_desc
    }

    response = requests.post(api_url, json=payload, headers=headers)
    
    logger.info("M-Pesa STKPush Request Payload: %s", payload)
    logger.info("M-Pesa STKPush Response: %s", response.text)

    return response.json()


