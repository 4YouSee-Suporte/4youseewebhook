import pytest
from model_bakery import baker


@pytest.fixture
def usuario_logado(db, django_user_model):
    """
    Cria um usuário fake usando a lib model_bakery.
    :param db: Acesso ao banco de dados.
    :param django_user_model: função de pytest que me traz a clase de criação de um usuário.
    :return: usuário com suas credenciais de acesso.
    """
    usuario_modelo = baker.make(django_user_model, first_name="Fulanito")
    return usuario_modelo


@pytest.fixture
def client_com_usuario_logado(usuario_logado, client):
    """
    É minha aplicação web com o usuário logado.
    :param usuario_logado: criado acima, ele é um usuário logado sem necessidade de setar usuário e senha.
    :param client: significa a sessão da minha aplicação web
    :return: client com o usuário logado
    """
    client.force_login(usuario_logado)
    return client
