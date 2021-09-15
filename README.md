<h1 align="center" >
    4YouSee Webhook <br>
    <img alt="GitHub followers" src="https://img.shields.io/github/followers/4YouSee-Suporte?label=Follow%20me%20%3A%29&style=social">
</h1>

<h3>⚈ Sobre este Projeto</h3>

Aplicação web desenvolvida em framework Django usando linguagem de programação Python. Nele é possível é possível adicionar várias contas para que dessa forma seja possível obter os dados delas num lugar só. Desta forma fica centralizado o gerenciamento e monitoramento de várias contas.

Você pode acessar na conta a partir dessa rota https://webhook-4uc.herokuapp.com. Pode solicitar o usuário e senha ao e-mail suporte@4yousee.com.br o seguir os seguintes passos para rodar o projeto no seu computador.


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

3. Configurar um banco de dados.

    Você precisa ter um banco de dados para rodar o projeto. Deve adicionar a variável `DATABASE_URL` no arquivo `.env` criado no passo anterior e colocar nele a endereçõ no formato URI, como é mostrado no seguinte exemplo:
    
    ```
    DATABASE_URL = mysql://username:password@host:100/nome_do_banco
    ```
4. Instalação do Projeto no Banco de dados.

    Todo projeto django possui seus arquivos prontos para se adaptar a um banco de dados, e por isso para instalar o projeto num banco de dados, é necessário migrar os dados para o banco com o seguinte comando desde o terminal
    
    ```
    python manage.py migrate
    ```
    
5. Criando super usuário.

    O super usuário é necessário porque o projeto precisa de um usuário que consiga ter todas as permissões. A primeira funcionalidade do super user é criar outros usuários. Para criar ele basta executar a seguinte na linha de comando:
    
    ```
    python manage.py createsuperuser
    ```

<hr>

<h3>⚈ Executando o Projeto </h3>

Para rodar o projeto basta com executar a seguinte linha no terminal, lembrando ter o ambiente isolado ativo.

    python manage.py runserver
    
<hr>

<h3>⚈ Features </h3>

<h4> Paths </h4>

O projeto possui os seguintes caminhos:
    
- `/` : (home)
- `/conta/` : (conta_detalhe)
- `/relatorio/` :(solicitar_relatorio)
- `/playlogs/` :(playlogs)

<h4> Home </h4>

Tela principal que exibe as contas adicionadas a partir da URL e token.

![image](https://user-images.githubusercontent.com/63620799/133329928-2a7c141d-69e5-44d4-94fe-73a5544f908a.png)


<h4> Detalhe de uma Conta </h4>

Tela que apresenta as informações de players, categorias, contas, playlists e playlogs de uma conta em específico.

![image](https://user-images.githubusercontent.com/63620799/133330362-3bd18caa-4d62-4f82-8237-15edcb063678.png)


<h4> Solicitar Relatório </h4>

Tela para solicitar relatórios de uma conta em específico. Considera todos os playlogs do día desde 00:00:00 até 23:59:59 

![image](https://user-images.githubusercontent.com/63620799/133330574-58c5ac48-e4e6-432e-97d0-a7d157534768.png)


<h4> Playlogs </h4>

Tela que exibe todos os playlogs existentes na aplicação separados por conta, e por día. Além esse path serve de webhook para receber a resposta da api do manager ao momento de solicitar um report.

![image](https://user-images.githubusercontent.com/63620799/133330807-e11d1ac3-0583-4984-bda3-4c8ec13f6e9d.png)

