import requests

token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI4ODI3MTEyLCJqdGkiOiI0NWU2ZWE5NWFmNWU0YThjYTlkNmMxMjc2YWZjYTNmYiIsInVzZXJfaWQiOjQ0fQ.vCDWcKwG7ahg1eLJFkJ_n3caLlnSc8jap-g5kPcp8VY"
headers = {'Authorization': 'JWT {}'.format(token)}

params = {
'ticker': 'PETR4',
'ano_tri': '20241T',
}

r = requests.get('https://laboratoriodefinancas.com/api/v1/balanco',params=params, headers=headers)
print(r.json())