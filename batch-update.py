import requests
from auth import authenticate

def get_contact_etag(resource_name, headers):
    # URL da API do Google People para buscar o contato
    url = f'https://people.googleapis.com/v1/{resource_name}'

    # Faz a requisição GET para obter o contato
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        contact = response.json()
        return contact.get('etag')
    else:
        print(f"Falha ao buscar o contato {resource_name}: {response.status_code} - {response.text}")
        return None

def update_batch_contacts(contact_updates):
    creds = authenticate()

    # Cabeçalhos de autenticação
    headers = {
        'Authorization': f'Bearer {creds.token}',
        'Content-Type': 'application/json',
    }

    # Para cada contato, buscar a etag e adicionar ao request
    for resource_name, update_data in contact_updates.items():
        etag = get_contact_etag(resource_name, headers)
        if etag:
            update_data['person']['etag'] = etag

    # URL da API do Google People para atualizar contatos em lote
    url = 'https://people.googleapis.com/v1/people:batchUpdateContacts'

    # Crie o corpo da requisição como um dicionário de mapas, onde cada chave é o resourceName do contato
    body = {
        "contacts": contact_updates,
        "updateMask": "emailAddresses,names",
        "readMask": "emailAddresses,names"
    }

    # Faz a requisição para a API Google People para atualizar os contatos em lote
    response = requests.post(url, headers=headers, json=body)

    # Verifica a resposta da API
    if response.status_code == 200:
        print("Usuários atualizados com sucesso!")
    else:
        print(f"Falha ao atualizar usuários em lote: {response.status_code} - {response.text}")

# Estrutura dos dados de atualização dos contatos
contact_updates = {
    "people/c4182492780001703024": {
            "names": [
                {
                    "givenName": "José Carlos",
                    "familyName": "Silva"
                }
            ],
            "emailAddresses": [
                {
                    "value": "jose.novo@teste.com",
                    "type": "work"
                }
            ]
    },
    "people/c8574440048907152179": {
            "names": [
                {
                    "givenName": "Ana Maria",
                    "familyName": "Silva Sousa"
                }
            ],
            "emailAddresses": [
                {
                    "value": "ana.silva.novo@teste.com",
                    "type": "work"
                }
            ]
    }
}

# Atualiza os usuários em lote na API Google People
update_batch_contacts(contact_updates)
