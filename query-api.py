from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from auth import authenticate  

def get_all_contacts():
    creds = authenticate() 
    service = build('people', 'v1', credentials=creds)
    all_contacts = []
    next_page_token = None

    try:
        while True:
            results = service.people().connections().list(
                resourceName='people/me',
                pageSize=2000,
                pageToken=next_page_token,
                personFields='names,emailAddresses,phoneNumbers,birthdays').execute()

            connections = results.get('connections', [])
            print(f"Found {len(connections)} connections in this page.")

            if not connections and not next_page_token:
                print("No more contacts found.")
                break

            all_contacts.extend(connections)
            next_page_token = results.get('nextPageToken')
            if not next_page_token:
                break

        if not all_contacts:
            print("No contacts found at all.")
        else:
            # Remover contatos duplicados
            unique_contacts = {contact['resourceName']: contact for contact in all_contacts}.values()

            for person in unique_contacts:
                names = person.get('names', [])
                emails = person.get('emailAddresses', [])
                phones = person.get('phoneNumbers', [])
                birthdays = person.get('birthdays', [])

                if names:
                    print(f"Name: {names[0].get('displayName')}")
                if emails:
                    print(f"Email: {emails[0].get('value')}")
                if phones:
                    print(f"Phone: {phones[0].get('value')}")
                if birthdays:
                    bday = birthdays[0].get('date')
                    print(f"Birthday: {bday.get('day')}/{bday.get('month')}/{bday.get('year')}")
                print("-" * 40)  # Separador

            print(f"Total de Contatos Cadastrados: {len(unique_contacts)}")

    except HttpError as e:
        print(f"Ocorreu um erro: {e}")

def main():
    get_all_contacts()

if __name__ == '__main__':
    main()
