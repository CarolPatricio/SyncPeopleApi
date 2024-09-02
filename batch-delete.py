import requests
from auth import authenticate

def delete_batch_contact(resource_names):
    creds = authenticate()

    # URL da API do Google People para deletar em lote contatos
    url = 'https://people.googleapis.com/v1/people:batchDeleteContacts'

    # Cabeçalhos de autenticação
    headers = {
        'Authorization': f'Bearer {creds.token}',
        'Content-Type': 'application/json',
    }

    body = {
        "resourceNames": resource_names
    }

    response = requests.post(url, headers=headers, json=body)

    if response.status_code == 200:
        print("Usuários deletados com sucesso!")
    else:
        print(f"Falha ao deletar usuários em lote: {response.status_code} - {response.text}")

# Lista de resourceNames dos contatos a serem deletados
resource_names = [
    "people/c5730661536192716159",
    "people/c5850935208419985973",
]

def main():
    delete_batch_contact(resource_names)

if __name__ == '__main__':
    main()
