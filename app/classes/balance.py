import requests
import json


class Balance():

    def __init__(self):
        with open('conf.json', 'r') as file:
            config = json.load(file)
        self.selectel_accounts = config['selectel_accounts']

    def get_balance(self, account_id, user, password):
        url = 'https://cloud.api.selcloud.ru/identity/v3/auth/tokens'
        headers = {
            'Content-Type': 'application/json',
        }

        data = {
            "auth": {
                "identity": {
                    "methods": ["password"],
                    "password": {
                        "user": {
                            "name": user,
                            "domain": {"name": str(account_id)},
                            "password": password
                        }
                    }
                },
                "scope": {
                    "domain": {
                        "name": str(account_id)
                    }
                }
            }
        }
        response = requests.post(url, headers=headers, json=data)
        token = response.headers.get('X-Subject-Token')
        balance_url = "https://api.selectel.ru/v3/billing/balance"
        headers = {
            'X-Auth-Token': token
        }

        balance_response = requests.get(balance_url, headers=headers)
        balance_info = balance_response.json()
        prediction_url = "https://api.selectel.ru/v2/billing/prediction"
        headers = {
            'X-Auth-Token': token
        }
        prediction_response = requests.get(prediction_url, headers=headers)
        prediction_info = prediction_response.json()
        balance = balance_info['data']['primary']['main'] / 100
        prediction = prediction_info['data']['primary']

        return {'balance': balance, 'hours_remaining': prediction}

    def get_all_balances(self):
        result = []
        for account in self.selectel_accounts:
            account_note = {
                'account_id': account['account_id'], 'balance': 0, 'hours_remaining': 0, 'status': 'ok'}
            data = None
            try:
                data = self.get_balance(
                    account['account_id'], account['user'], account['password'])
            except Exception as exc:
                account_note['status'] = exc
            if data:
                if data['balance']:
                    account_note['balance'] = data['balance']
                if data['hours_remaining']:
                    account_note['hours_remaining'] = data['hours_remaining']
            result.append(account_note)
        return result
