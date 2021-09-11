<h1 align="center" >
    4YouSee Webhook <br>
    <img alt="GitHub stars" src="https://img.shields.io/github/stars/4YouSee-Suporte/4youseewebhook?style=social">
    <img alt="GitHub followers" src="https://img.shields.io/github/followers/4YouSee-Suporte?label=Follow%20me%20%3A%29&style=social">
</h1>

<h3>⚈ Sobre este Projeto'</h3>

Aplicativo web que permite adicionar várias contas para que dessa forma seja possível obter os dados dessas contas num lugar só.


<h3>⚈ Requisitos</h3>

Pip, Python instalados e configurados como variáveis de ambiente.

1. Criar uma pasta e dentro dela execute os seguintes comandos:

- Para isolar o ambiente:

    ```
    python -m venv .venv
    ```

- Para ativar o ambiente isolado:

    | Windows                   | Linux                        |
    |---------------------------|------------------------------|
    |`\Scripts\activate.bat`    | `source .venv/bin/activate`  |

- Instalando as dependencias:

    ```
    pip install -r requirements.txt
    ```
    
2. Criar arquivo `.env` na raiz, com as seguintes variáveis:
 
    `DEBUG = True`
    
    `SECRET_KEY` = 
    
     Para preencher as seguintes variáveis você pode usar sua conta de gmail (por exemplo) ou usar outros proveedores como mailgun, mailchimp, sendgrid, etc.
    
    `EMAIL_USE_TLS` = True
    
    `EMAIL_HOST` = 
    
    `EMAIL_PORT` = 587
    
    `EMAIL_HOST_USER` = 
    
    `EMAIL_HOST_PASSWORD` = 
    
    `EMAIL_BACKEND` = django.core.mail.backends.smtp.EmailBackend

    #### Como gerar o SECRET_KEY ?
    Para gerar o SECRET_KEY, crie primeiramente o arquivo .env e adicione todas as variáveis anteriormente mencionadas com valores vazíos. Enseguida, execute `python manage.py shell` e digite o seguinte:
    ```
    >>> from django.core.management.utils import get_random_secret_key
    >>> get_random_secret_key()
    908ads768/*>-06&6a # Esse é valor que deve ser colocado no .env na variável SECRET_KEY
    ```

3. Fazer as migrações para o banco.

    Executar o seguinte:

    ```
    >>> python manage.py migrate
    ```
    
