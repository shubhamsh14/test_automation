import requests
import urllib3
urllib3.disable_warnings()
from flask import jsonify

def get_token(login_data):
    try:
        url = "https://202.38.173.223:1280/api/v3/token"
        payload = {
          "grant_type": "password",
          "username": login_data['username'],
          "password": login_data['password']
        }
        headers = {
          "Content-Type": "application/x-www-form-urlencoded",
          "X-Client-Version": "string"
        }
      
        response = requests.post(url, data=payload, headers=headers, verify=False)

        # Check the response status code
        if response.status_code == 200:
            json_response = response.json()
            return json_response.get('access_token')
        else:
            print(f"Failed to get token. Status code: {response.status_code}")
            return 'Login failed'
    except Exception as e:
        # Handle other exceptions (e.g., network issues)
        print(f"An error occurred: {str(e)}")
        return 'Login failed'


def create_reseller(token, login_data, user_data):
    if token != 'login failed':
        try:
            url = "https://202.38.173.223:1280/api/v3/organizations/resellers"
            payload = {
                "description": "Reseller for New Site",
                "organizationInput": {
                    "name": user_data['name'],
                    "email": user_data['email'],
                    "phone": user_data['contact'],
                },
                "quota": {
                    "serversQuota": 50,
                    "isServersQuotaUnlimited": False,
                    "workstationsQuota": 50,
                    "isWorkstationsQuotaUnlimited": False,
                },
                "ownerCredentials": {
                    "userName": user_data['username'],
                    "password": user_data['password']
                },
                "permissions": [
                    "REST"
                ]
            }
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token,
                "accept": "application/json"
            }
            response = requests.post(url, json=payload, headers=headers, verify=False)

            # Check the response status code
            if response.status_code == 200:
                data = response.json()
                return data
            elif response.status_code == 400:
                json_response = response.json()
                errors = json_response.get('errors', [])
                # Check if the 'propertyName' is present in the errors and return its value
                try:
                    for error in errors:
                        if 'propertyName' in error and error['propertyName'] == 'OwnerCredentials.UserName':
                            return f'UserName : "{user_data['username']}" already exist'

                    print(f"Failed to create reseller. Status code: {response.status_code}")
                    return 'Reseller Not Created.'
                except Exception as e:
                    # Handle other exceptions (e.g., network issues)
                    print(f"An error occurred: {str(e)}")
            else:
                print(f"Failed to create reseller. Status code: {response.status_code}")
                return 'Reseller Not Created.'

        except Exception as e:
            # Handle other exceptions (e.g., network issues)
            print(f"An error occurred: {str(e)}")
            return 'Reseller Not Created.'

        
def send_welcome_mail(reseller_uid,user_data, token):
    url = "https://202.38.173.223:1280/api/v3/organizations/resellers/" + reseller_uid + "/welcomeEmail"
    payload = {
        "password": user_data['password']
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token,
        "accept": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers, verify=False)

        # Check the response status code
        if response.status_code == 200:
            data = response.json()
            print(response)
            return 'Resellers Created successfully and Welcome email sent.'
        else:
            print(f"Failed to send welcome email. Status code: {response.status_code}")
            return 'Reseller Created, Welcome email not sent.'
    except Exception as e:
        # Handle other exceptions (e.g., network issues)
        print(f"An error occurred: {str(e)}")
        return 'Welcome email not sent.'
