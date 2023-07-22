
from flask import Flask, render_template, request, redirect, session, url_for
import requests
import geocoder
import base64
import traceback
import json
last=[]
iso_to_dialing_code = {
    'AF': '+93',  # Afghanistan
    'AL': '+355',  # Albania
    'DZ': '+213',  # Algeria
    'AD': '+376',  # Andorra
    'AO': '+244',  # Angola
    'AR': '+54',   # Argentina
    'AM': '+374',  # Armenia
    'AU': '+61',   # Australia
    'AT': '+43',   # Austria
    'AZ': '+994',  # Azerbaijan
    'BH': '+973',  # Bahrain
    'BD': '+880',  # Bangladesh
    'BY': '+375',  # Belarus
    'BE': '+32',   # Belgium
    'BZ': '+501',  # Belize
    'BJ': '+229',  # Benin
    'BT': '+975',  # Bhutan
    'BO': '+591',  # Bolivia
    'BA': '+387',  # Bosnia and Herzegovina
    'BR': '+55',   # Brazil
    'BN': '+673',  # Brunei
    'BG': '+359',  # Bulgaria
    'BF': '+226',  # Burkina Faso
    'BI': '+257',  # Burundi
    'KH': '+855',  # Cambodia
    'CM': '+237',  # Cameroon
    'CA': '+1',    # Canada
    'CV': '+238',  # Cape Verde
    'CF': '+236',  # Central African Republic
    'TD': '+235',  # Chad
    'CL': '+56',   # Chile
    'CN': '+86',   # China
    'CO': '+57',   # Colombia
    'KM': '+269',  # Comoros
    'CG': '+242',  # Congo
    'CD': '+243',  # Congo, Democratic Republic of the
    'CR': '+506',  # Costa Rica
    'HR': '+385',  # Croatia
    'CU': '+53',   # Cuba
    'CY': '+357',  # Cyprus
    'CZ': '+420',  # Czech Republic
    'DK': '+45',   # Denmark
    'DJ': '+253',  # Djibouti
    'EC': '+593',  # Ecuador
    'EG': '+20',   # Egypt
    'SV': '+503',  # El Salvador
    'GQ': '+240',  # Equatorial Guinea
    'ER': '+291',  # Eritrea
    'EE': '+372',  # Estonia
    'ET': '+251',  # Ethiopia
    'FJ': '+679',  # Fiji
    'FI': '+358',  # Finland
    'FR': '+33',   # France
    'GA': '+241',  # Gabon
    'GM': '+220',  # Gambia
    'GE': '+995',  # Georgia
    'DE': '+49',   # Germany
    'GH': '+233',  # Ghana
    'GR': '+30',   # Greece
    'GT': '+502',  # Guatemala
    'GN': '+224',  # Guinea
    'GW': '+245',  # Guinea-Bissau
    'GY': '+592',  # Guyana
    'HT': '+509',  # Haiti
    'HN': '+504',  # Honduras
    'HU': '+36',   # Hungary
    'IS': '+354',  # Iceland
    'IN': '+91',   # India
    'ID': '+62',   # Indonesia
    'IR': '+98',   # Iran
    'IQ': '+964',  # Iraq
    'IE': '+353',  # Ireland
    'IL': '+972',  # Israel
    'IT': '+39',   # Italy
    'JM': '+1',    # Jamaica
    'JP': '+81',   # Japan
    'JO': '+962',  # Jordan
    'KZ': '+7',    # Kazakhstan
    'KE': '+254',  # Kenya
    'KI': '+686',  # Kiribati
    'KW': '+965',  # Kuwait
    'KG': '+996',  # Kyrgyzstan
    'LA': '+856',  # Laos
    'LV': '+371',  # Latvia
    'LB': '+961',  # Lebanon
    'LS': '+266',  # Lesotho
    'LR': '+231',  # Liberia
    'LY': '+218',  # Libya
    'LI': '+423',  # Liechtenstein
    'LT': '+370',  # Lithuania
    'LU': '+352',  # Luxembourg
    'MG': '+261',  # Madagascar
    'MW': '+265',  # Malawi
    'MY': '+60',   # Malaysia
    'MV': '+960',  # Maldives
    'ML': '+223',  # Mali
    'MT': '+356',  # Malta
    'MH': '+692',  # Marshall Islands
    'MR': '+222',  # Mauritania
    'MU': '+230',  # Mauritius
    'MX': '+52',   # Mexico
    'FM': '+691',  # Micronesia
    'MD': '+373',  # Moldova
    'MC': '+377',  # Monaco
    'MN': '+976',  # Mongolia
    'ME': '+382',  # Montenegro
    'MA': '+212',  # Morocco
    'MZ': '+258',  # Mozambique
    'MM': '+95',   # Myanmar
    'NA': '+264',  # Namibia
    'NR': '+674',  # Nauru
    'NP': '+977',  # Nepal
    'NL': '+31',   # Netherlands
    'NZ': '+64',   # New Zealand
    'NI': '+505',  # Nicaragua
    'NE': '+227',  # Niger
    'NG': '+234',  # Nigeria
    'KP': '+850',  # North Korea
    'NO': '+47',   # Norway
    'OM': '+968',  # Oman
    'PK': '+92',   # Pakistan
    'PW': '+680',  # Palau
    'PA': '+507',  # Panama
    'PG': '+675',  # Papua New Guinea
    'PY': '+595',  # Paraguay
    'PE': '+51',   # Peru
    'PH': '+63',   # Philippines
    'PL': '+48',   # Poland
    'PT': '+351',  # Portugal
    'QA': '+974',  # Qatar
    'RO': '+40',   # Romania
    'RU': '+7',    # Russia
    'RW': '+250',  # Rwanda
    'KN': '+1',    # Saint Kitts and Nevis
    'LC': '+1',    # Saint Lucia
    'VC': '+1',    # Saint Vincent and the Grenadines
    'WS': '+685',  # Samoa
    'SM': '+378',  # San Marino
    'ST': '+239',  # Sao Tome and Principe
    'SA': '+966',  # Saudi Arabia
    'SN': '+221',  # Senegal
    'RS': '+381',  # Serbia
    'SC': '+248',  # Seychelles
    'SL': '+232',  # Sierra Leone
    'SG': '+65',   # Singapore
    'SK': '+421',  # Slovakia
    'SI': '+386',  # Slovenia
    'SB': '+677',  # Solomon Islands
    'SO': '+252',  # Somalia
    'ZA': '+27',   # South Africa
    'KR': '+82',   # South Korea
    'SS': '+211',  # South Sudan
    'ES': '+34',   # Spain
    'LK': '+94',   # Sri Lanka
    'SD': '+249',  # Sudan
    'SR': '+597',  # Suriname
    'SZ': '+268',  # Eswatini
    'SE': '+46',   # Sweden
    'CH': '+41',   # Switzerland
    'SY': '+963',  # Syria
    'TW': '+886',  # Taiwan
    'TJ': '+992',  # Tajikistan
    'TZ': '+255',  # Tanzania
    'TH': '+66',   # Thailand
    'TL': '+670',  # Timor-Leste
    'TG': '+228',  # Togo
    'TO': '+676',  # Tonga
    'TT': '+1',    # Trinidad and Tobago
    'TN': '+216',  # Tunisia
    'TR': '+90',   # Turkey
    'TM': '+993',  # Turkmenistan
    'TV': '+688',  # Tuvalu
    'UG': '+256',  # Uganda
    'UA': '+380',  # Ukraine
    'AE': '+971',  # United Arab Emirates
    'GB': '+44',   # United Kingdom
    'US': '+1',    # United States
    'UY': '+598',  # Uruguay
    'UZ': '+998',  # Uzbekistan
    'VU': '+678',  # Vanuatu
    'VA': '+39',   # Vatican City
    'VE': '+58',   # Venezuela
    'VN': '+84',   # Vietnam
    'YE': '+967',  # Yemen
    'ZM': '+260',  # Zambia
    'ZW': '+263',  # Zimbabwe
}

app = Flask(__name__)
app.secret_key = 'your-secret-key'
app.config['DEBUG'] = True
CLIENT_ID = 'KKLjJZ3r-MfdC0Clb-PgL6S4CP-t8mh3NQl'
CLIENT_SECRET = 'T0XF6QRcOyohRsLwKjSNs94d8XmEKNPU'
REDIRECT_URI = 'http://apicash.pythonanywhere.com/callback'
def get_options(data):
 options={}
 for el in data:
  eg= el.get('supportedCountries')
  for e in eg:
     if e in options.keys():
         print(e,"already exist")
         options[e].append({"name":el["name"],"id":el["id"]})
     else:
         options[e]=[{"name":el["name"],"id":el["id"]}]
         print(e,"will be created")
 return options
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
@app.route('/add-money', methods=['POST','GET'])
def add_money():
 try:   
    if request.method == 'POST':
        payment_method = request.form['payment_method']
        amount = request.form['amount']
        currency = request.form['currency']
        country = request.form.get('country', '')
        customer = request.form['customer']
        number = request.form.get('iso', '')+request.form.get('number', '')
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
           
            'return_url': return_url,
            'cancel_url': cancel_url
        }
       
        if agent_in_hand:
          data.update({ 'agentId': agent_id,
            'agentInHand': agent_in_hand})
        for k,v in data.copy().items():
          if v=="":
            del data[k]
           
        # Make the API request to add money
        response = requests.post('https://www.awdpay.com/api/v1/deposits', headers=headers, data=data)

        if response.status_code == 200:
            # Request successful, handle the response
            # ...
            if payment_method in [17,"17",21,"21"]:
             rs=response.json()
             return redirect(url_for('add_money_confirmation',instructions=str(rs), extras=rs.get('extra')))  # Replace with your desired success route
            else:
             response_data=response.json()
             tex=response.text
           #  redirect_url = response_data.get("redirect")
             headers = {
            'Authorization': 'Bearer ' + access_token,
            'Content-Type': 'application/x-www-form-urlencoded'
        }
             rg=response_data.get('extra')
             data = {
            'extra': rg}
        # Make the API request to confirm the deposit
             if rg:
              response = requests.post('https://www.awdpay.com/api/v1/deposits/confirm', headers=headers, data=data)
              return response.text+"--"+tex+"++"+str(response_data) #str(response_data)#redirect(redirect_url)#requests.post(redirect_url, data=response_data).text
             else:
              id=response_data.get('id')
              last.clear()
              last.append(id)
              
              return redirect(url_for('lastc')) 
        else:
            # Request failed, handle the error
            # ...
            return response.text+"--"+str(data)+"++"+str(response.json())  # Replace with your desired failure route
 except:
     return traceback.format_exc() 
@app.route('/add-money/<string:dts>', methods=['GET'])
def add_money_id(dts):
 try:   
    image_id,iso=dts.split("-")
    dc=iso_to_dialing_code[iso]
    return render_template('add-money.html',theid=int(image_id),iso=iso,dc=dc)
 except:
     return traceback.format_exc()
@app.route('/add-money-confirmation', methods=['GET', 'POST'])
def add_money_confirmation():
    instruction = request.args.get('instructions') 
    extra = request.args.get('extras') 
    if request.method == 'POST':
        
        
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
            return response.text#redirect(url_for('failure'))  # Replace with your desired failure route

    return render_template('add-money-confirmation.html',instruction=instruction)

@app.route('/success')
def success():
    return render_template('success.html')
@app.route('/deposit')
def get_list():
 try:
        access_token = generate_access_token()

        # Prepare the request data
        headers = {
            'Authorization': 'Bearer ' + access_token,
            'Content-Type': 'application/x-www-form-urlencoded'
        }    

        url="https://www.awdpay.com/api/v1/gateways"
        response = requests.get(url, headers=headers)
        data_dict=get_options(json.loads(response.text)['data'])
        keys = list(data_dict.keys())
        return render_template('gateway_deposit.html', keys=keys, data_dict_json=data_dict)
 except:
     return traceback.format_exc()
@app.route('/failure')
def failure():
    return render_template('failure.html')
@app.route('/last')
def lastc():
 try:
    # Generate the access token
    access_token = generate_access_token()

        # Prepare the request data
    headers = {
            'Authorization': 'Bearer ' + access_token,
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    return  requests.get('https://www.awdpay.com/api/v1/deposits/'+str(last[-1]), headers=headers).text
 except: 
  return traceback.format_exc() 
@app.route('/')
def bonjour():
    return "Bonjour c est bahae el hmimdi le devlopeur"    
@app.route('/depositi/<int:image_id>')
def depositi(image_id):
    # Do something with the image_id, for example, render a template or process the ID.
    return f"Deposit Page for ID: {image_id}" 

if __name__ == '__main__':
    app.run(debug=True)
