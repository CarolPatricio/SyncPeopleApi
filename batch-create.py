import requests
from auth import authenticate

def get_data_from_mock_api():
    response = requests.get('http://localhost:5000/mock-api')
    return response.json()

def process_data():
    process_contact = []
    data = get_data_from_mock_api()

    aligned_records = []

    #Associar campos ao valores
    for record in data['message']['values']:
        aligned_record = {}
        for field, value in zip(data['message']['fields'], record['record']):
            aligned_record[field['fieldName']] = value['value']
        aligned_records.append(aligned_record)

    #Obter valores dos campos necessários
    for rec in aligned_records:
        registration = rec['Id']
        name_full = rec['Nome_completo']
        email = rec['Email']
        ua = rec['Hierarquia_ua']
        building =  rec['Predio']
        room = rec['Sala']
        birthday = rec['Data_nascimento']
        phone = rec['Celular_corporativo']
        directorate =  rec['Sigla_diretoria']
        
        #Processar informações necessárias
        name_parts = name_full.split(' ', 1)
        given_name = name_parts[0]
        family_name = name_parts[1] if len(name_parts) > 1 else ''
        birthday_parts = birthday.split('/')
        day = int(birthday_parts[0])
        month = int(birthday_parts[1])

        contact_body = {
            "contactPerson": {
                "names": [
                    {
                        "givenName": given_name,
                        "familyName": family_name
                    }
                ],
                "emailAddresses": [
                    {
                        "value": email,
                        "type": "Trabalho"
                    }
                ],
                "phoneNumbers": [
                    {
                        "value": phone,
                        "type": "Trabalho",
                    }
                ],
                "birthdays": [
                    {
                        "date": {
                            "day": day,
                            "month": month
                        }
                    }
                ],
                "addresses": [
                        {
                            "streetAddress": "Prédio" + building,
                            "extendedAddress": room,
                            "type": "Local do escritório",
                        }
                ],
                "organizations": [
                    {
                        "name": ua, 
                        "department":  directorate,
                        "title": registration,
                        "type": "Trabalho",
                    }
                ]
            }
        }

        process_contact.append(contact_body)
    
    return process_contact

def create_batch_contacts(process_contact):
    creds = authenticate()

    # URL da API do Google People para criação em lote de contatos
    url = 'https://people.googleapis.com/v1/people:batchCreateContacts'

    headers = {
        'Authorization': f'Bearer {creds.token}',
        'Content-Type': 'application/json',
    }

    body = {
        "contacts": process_contact
    }

    response = requests.post(url, headers=headers, json=body)

    if response.status_code == 200:
        print("Usuários criados com sucesso!")
        print(response) 
    else:
        print(f"Falha ao criar usuários em lote: {response.status_code} - {response.text}")

def main():
    process_contact = process_data()
    create_batch_contacts(process_contact)

if __name__ == '__main__':
    main()