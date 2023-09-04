import requests
import json
#OBTEM O TOKEN VÁLIDO PARA REQUISIÇÕES DA API
def get_token_api_eventos():
    context = {
            "username":"admin",
            "password":"CETT@2023"
        }
    response = requests.post('https://regente.cett.org.br/token',data=context)
    if response.status_code == 200:
        token_data = response.json()
        token = token_data.get('access')
        return token
    else:
        print("Failed to get token. Status code:", response.status_code)

def get_all_eventos(token):
    headers = {'Authorization': f'Bearer {token}'}
    api_url = 'https://regente.cett.org.br/dp-eventos'
    response = requests.get(api_url, headers=headers)
    return json.loads(response.content)

def get_evento(token,id):
    headers = {'Authorization': f'Bearer {token}'}
    api_url = f'https://regente.cett.org.br/dp-eventos/{id}'
    response = requests.get(api_url, headers=headers)
    return json.loads(response.content)