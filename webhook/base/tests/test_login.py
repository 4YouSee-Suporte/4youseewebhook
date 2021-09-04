import pytest
from django.urls import reverse
from model_bakery import baker

from webhook.django_assertions import assert_contains


@pytest.fixture
def resp(client, db):
    return client.get(reverse('login'))


def test_login_form_page(resp):
    assert resp.status_code == 200


@pytest.fixture
def usuario(db, django_user_model):
    """
    Cria um usuário fake usando a lib model_bakery.
    :param db: Acesso ao banco de dados.
    :param django_user_model: função de pytest que me traz a clase de criação de um usuário.
    :return: usuário com suas credenciais de acesso.
    """
    usuario_modelo = baker.make(django_user_model)
    senha = 'senha'
    usuario_modelo.set_password(senha)  # Gera o hash baseado na senha criada na linha anterior
    usuario_modelo.save()
    usuario_modelo.senha_plana = senha
    return usuario_modelo


@pytest.fixture
def resp_post(client, usuario):
    """
    Emulando o envio das credenciais de um usuário na tela de login.
    Em outras palavras: enviando um post com alguns dados para uma url.
    :param client: É minha sessão da aplicação.
    :param usuario: usuario criado acima com username e senha_plana
    :return: resposta de fazer um post na url login com os dados do usuário como contexto do post.
    """
    return client.post(reverse('login'), {'username': usuario.username, 'password': usuario.senha_plana})


def test_login_redirect(resp_post):
    assert resp_post.status_code == 302
    assert resp_post.url == reverse('manager:home')


@pytest.fixture
def resp_home_com_usuario_logado(client_com_usuario_logado, db):
    """
    Emulando o login sem necessáriamente enviar os dados de login.
    :param client_com_usuario_logado: Criado em conftest.py. ele é um usuário logado.
    :param db:
    :return:
    """
    return client_com_usuario_logado.get(reverse('base:home'))


def test_botao_salir_disponivel(resp_home_com_usuario_logado):
    assert_contains(resp_home_com_usuario_logado, 'Salir')


def test_nome_usuario_logado_disponivel(resp_home_com_usuario_logado, usuario_logado):
    assert_contains(resp_home_com_usuario_logado, usuario_logado.first_name)


def test_link_logout_disponivel(resp_home_com_usuario_logado):
    assert_contains(resp_home_com_usuario_logado, reverse('logout'))
