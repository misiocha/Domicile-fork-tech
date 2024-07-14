from flask import Flask, render_template, request, jsonify
import requests
from requests.auth import HTTPBasicAuth
import base64
import json
from datetime import datetime

app = Flask(__name__)

# Mpesa API Credentials
consumer_key = "YK4AMQubZhHBZi45pV68X8oLjw2PJLGlsMuwiaRqHEWG1RcL"
consumer_secret = "GqHPQT8JWAHdumv59zlAKnhJlwzH2IOGGGzaSU5SHtsvZwzTZw0p7jYxwDXuINcF"
shortcode = 'your_shortcode'
lipa_na_mpesa_online_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
access_token_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
callback_url = 'https://your_callback_url'  # Ensure this URL is publicly accessible

# Generate the Mpesa access token
def generate_access_token():
    response = requests.get(access_token_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(response.text)
    return mpesa_access_token['access_token']

# Generate Mpesa password
def generate_password(shortcode, passkey):
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    password_str = f"{shortcode}{passkey}{timestamp}"
    password = base64.b64encode(password_str.encode()).decode('utf-8')
    return password, timestamp

# Make a payment request
@app.route('/make_payment', methods=['POST'])
def make_payment():
    data = request.get_json()
    access_token = generate_access_token()
    password, timestamp = generate_password(shortcode, 'your_passkey')
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    payload = {
        "BusinessShortCode": shortcode,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": data['amount'],
        "PartyA": data['phone'],
        "PartyB": shortcode,
        "PhoneNumber": data['phone'],
        "CallBackURL": callback_url,
        "AccountReference": "DomicileForkTechnologies",
        "TransactionDesc": "Payment for services"
    }
    response = requests.post(lipa_na_mpesa_online_url, json=payload, headers=headers)
    return jsonify(response.json())

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
