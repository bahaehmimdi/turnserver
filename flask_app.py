
from flask import Flask, render_template, request, redirect, session, url_for
import requests
import geocoder
import base64
app = Flask(__name__)
app.secret_key = 'your-secret-key'

CLIENT_ID = 'KKLjJZ3r-MfdC0Clb-PgL6S4CP-t8mh3NQl'
CLIENT_SECRET = 'T0XF6QRcOyohRsLwKjSNs94d8XmEKNPU'
REDIRECT_URI = 'http://apicash.pythonanywhere.com/callback'

def get_user_location():
    g = geocoder.ip('me')
    return g.country

def generate_access_token():
    # Encode the client credentials as Base64
    credentials = f'{CLIENT_ID}:{CLIENT_SECRET}'
    encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')

    # Make the API request to generate the access token
    token_url = 'https://www.awdpay.com/api/v1/token'
    headers = {'Authorization': 'Basic ' + encoded_credentials}

    response = requests.post(token_url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Extract the access token from the response
        access_token = response.json().get('access_token')
        return access_token
    else:
        # Request failed, handle the error
        print('Access token generation failed. Error:', response.text)
        return  response.text
@app.route('/generate-token')
def generate_token():
    # Replace '[userkey]' and '[secretkey]' with your actual user key and secret key
    #user_key = '[userkey]'
   # secret_key = '[secretkey]'

    # Generate the access token
    access_token = generate_access_token()

    return access_token
@app.route('/add-money', methods=['GET', 'POST'])
def add_money():
    if request.method == 'POST':
        payment_method = request.form['payment_method']
        amount = request.form['amount']
        currency = request.form['currency']
        country = request.form.get('country', '')
        customer = request.form['customer']
        number = request.form.get('number', '')
        agent_id = request.form.get('agent_id', '')
        agent_in_hand = request.form.get('agent_in_hand', False)
        return_url = request.form.get('return_url', '')
        cancel_url = request.form.get('cancel_url', '')

        # Generate the access token
        access_token = generate_access_token()

        # Prepare the request data
        headers = {
            'Authorization': 'Bearer ' + access_token,
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'payment_method': payment_method,
            'amount': amount,
            'currency': currency,
            'country': country,
            'customer': customer,
            'number': number,
            'agentId': agent_id,
            'agentInHand': agent_in_hand,
            'return_url': return_url,
            'cancel_url': cancel_url
        }

        # Make the API request to add money
        response = requests.post('https://www.awdpay.com/api/v1/deposits', headers=headers, data=data)

        if response.status_code == 200:
            # Request successful, handle the response
            # ...
            return redirect(url_for('success'))  # Replace with your desired success route
        else:
            # Request failed, handle the error
            # ...
            return redirect(url_for('failure'))  # Replace with your desired failure route

    return render_template('add-money.html')

@app.route('/add-money-confirmation', methods=['GET', 'POST'])
def add_money_confirmation():
    if request.method == 'POST':
        extra = request.form['extra']
        otp = request.form['otp']

        # Generate the access token
        access_token = generate_access_token()

        # Prepare the request data
        headers = {
            'Authorization': 'Bearer ' + access_token,
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'extra': extra,
            'otp': otp
        }

        # Make the API request to confirm the deposit
        response = requests.post('https://www.awdpay.com/api/v1/deposits/confirm', headers=headers, data=data)

        if response.status_code == 200:
            # Request successful, handle the response
            # ...
            return redirect(url_for('success'))  # Replace with your desired success route
        else:
            # Request failed, handle the error
            # ...
            return redirect(url_for('failure'))  # Replace with your desired failure route

    return render_template('add-money-confirmation.html')

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/failure')
def failure():
    return render_template('failure.html')
@app.route('/')
def bonjour():
    return "Bonjour c est bahae el hmimdi le devlopeur"    
if __name__ == '__main__':
    app.run(debug=True)