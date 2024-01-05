from flask import Flask, render_template, request
import configparser
from auth import get_token, create_reseller, send_welcome_mail
app = Flask(__name__)

# Read API credentials from config file
config = configparser.ConfigParser()
config.read('config.ini')
login_credentials = {
'username' : config.get('login_credentials', 'username'),
'password' : config.get('login_credentials', 'password')}

def process_reseller(user_data):
    token = get_token(login_credentials)
    if token != 'Login failed':

        response = create_reseller(token, login_credentials, user_data)
        print('response', response)
        if isinstance(response, str):
            print(123)
            return response
        else:
            print(457)
            reseller_uid = response['data']['quota']['resellerUid']
            email_flag = send_welcome_mail(reseller_uid, user_data, token )
            return email_flag
    else:
        return "Processing unsuccessful, please retry after some time."


@app.route('/')
def index():
    return render_template('form.html')



@app.route('/create_resellers', methods=['POST'])
def submit_form():
    try:
        # Get the JSON data from the form
        data = request.form.items
              # Check if 'data' is not None
        if data is not None:
            # Parse the JSON dat

            # Access attributes based on keys
            user_data = {
            'name': request.form.get('name', ''),
            'contact' : request.form.get('contact', ''),
            'email' : request.form.get('email', ''),
            'company' : request.form.get('company', ''),
            'username' : request.form.get('username', ''),
            'password' : request.form.get('password', '')}
            
            result = process_reseller(user_data)
            print(result)
            return f"<p style='color: #ff6900; font-size: 18px; font-family: \"Courier 10 Pitch\";'>{result}</p>" 
        else:
            return "<p style='color: #ff6900; font-size: 18px; font-family: \"Courier 10 Pitch\";'>Fill the details</p>"
    except Exception as e:
        return "<p style='color: #ff6900; font-size: 18px; font-family: \"Courier 10 Pitch\";'>Please Try again</p>"


if __name__ == '__main__':
    app.run(debug=True)
