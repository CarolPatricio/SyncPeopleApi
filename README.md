# 👤 SyncPeopleApi 

Este projeto em Python interage com o Google Contatos para gerenciar contatos em lote, incluindo listar, criar, atualizar e deletar. Utiliza uma API mockada construída com Flask para simular informações de colaboradores e realizar operações na People API.

## Instalação das Dependências
Para instalar as dependências necessárias, execute o seguinte comando:

```bash
    pip install -r requirements.txt
```

## Executar a API Mockada com Flask
Para iniciar a API mockada para conseguir criar contatos, utilize o comando:
 ```bash
    python app.py
```
## Executar Operações
Para executar uma operação específica, utilize o comando apropriado:
 ```bash
    python nome_do_arquivo.py
```
Certifique-se de substituir nome_do_arquivo.py pelo nome do script correspondente à operação que você deseja executar.

## Exemplos de Scripts

Aqui estão alguns exemplos de scripts disponíveis e suas funções:

- **query-api.py**: Lista todos os contatos.
- **batch-create.py**: Cria contatos em lote.
- **batch-update.py**: Atualiza contatos existentes em lote.
- **batch-delete.py**: Deleta contatos em lote.
- **auth.py**: Faz a autenticação com o Google Contatos e é chamada pelos demais scripts.
