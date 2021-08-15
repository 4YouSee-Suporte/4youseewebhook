import gzip
import io
import re
import requests
from django.db import IntegrityError

from webhook.base.models import Register


def bytes_to_dict(bytes_object):
    """
    Essa função recebe um objeto tipo bytes e retorna um diccionário.
    """
    try:
        my_dict = bytes_object.decode('utf8').replace("'", '"')
        return eval(my_dict)
    except UnicodeDecodeError:
        return {"message": "Não há logs na sua consulta"}


def process_file(bytesio_object):
    """
    Essa função recebe um BytesIO object que veio de um arquivo .gz, e retorna uma lista de dicionarios
    return : list of dicts: ['{"account":"alfareiza-3385E2","date":"2021-07-26","time":"15:58:52","playerId":4,"mediaId":48,"ip":"0.0.0.0","type":"I"}',
                    '{"account":"alfareiza-3385E2","date":"2021-07-26","time":"15:58:46"...]
    """
    data = []
    with gzip.GzipFile(fileobj=bytesio_object) as f:
        for line in f:
            data.append(bytes_to_dict(line))
        return data


def download_gz(url):
    """
    Essa função recebe a url do arquivo .gz que vai ler e logo retorna um BytesIO object
    param: str: 'https://4yousee-playlogs-reports.s3.amazonaws.com/alfareiza-3385E2/158549-6101805de1c1d.gz'
    return: BytesIO object
    """
    r = requests.get(url)
    r.raise_for_status()
    return io.BytesIO(r.content)


def name_of_account(url):
    """
    Recebe a url que possui o nome da conta que vem do relatório e retorna o nome só.
    reconhece ele se vem com o formato 'name' ou 'name-token'
    param: 'https://4yousee-playlogs-reports.s3.amazonaws.com/alfareiza-3385E2/158591-6102de52c5e5f.gz': str
    return: 'alfareiza-3385E2': str
    """
    if 'playlogs-reports' in url:
        return (url.split('/')[3])

    if '4yousee.com' in url:
        return re.findall('(\w+).4yousee.com', url)[0].capitalize()

    if '4usee.com' in url:
        return url.split('4usee.com')[1].split('/')[1].capitalize()


def insert_records(conta, data):
    """
    Recebe o objeto e inseri a data no banco de dados. A data são os logs de exibições recebidos do manager.
    param: conta : Account:
            data: list of dicts:
    return: records: int: Quantidade de registros inseridos
    """
    records = 0
    i = len(data) - 1
    while i:
        try:
            one_data = data[i]
            record_line = Register.objects.create(nickname=one_data['account'], date=one_data['date'],
                                                  time=one_data['time'], player_id=one_data['playerId'],
                                                  media_id=one_data['mediaId'], media_type=one_data['type'],
                                                  account=conta)
            records += 1
        except IntegrityError as e:
            pass
        except Exception as e:
            print('Error: ', e)
            pass
        i -= 1
    return records


def build_url(name_account):
    """
    >>> name_account = 'alfareiza-3385E2'
    >>> build_url(name_account)
    http://4usee.com/alfareiza/3385E2
    >>> name_account = 'tutorial'
    >>> build_url(name_account)
    http://tutorial.4yousee.com.br
    """
    if '-' in name_account:
        return f"http://4usee.com/{name_account.split('-')[0]}/{name_account.split('-')[1]}"
    else:
        return f"http://{name_account.split('-')[0]}.4yousee.com.br"


def enterprise_or_self(url):
    """
    Essa função recebe a url da conta e retorna 'enterprise' ou 'self' caso possua o formato correto.
    Caso não retorna um False
    param: str: url
    return: str: 'enterprise' 'self'
     >>> url = 'http://4usee.com/alfareiza/3385E2'
     >>> enterprise_or_self(url)
     'self'
     >>> url = 'http://tutorial.4yousee.com.br'
     >>> enterprise_or_self(url)
     'enterprise'
     >>> url = 'tutorial.4usee.com'
     >>> enterprise_or_self(url)
     False
     """
    if re.match('(http:\/\/|https:\/\/)?(\w+)\.4yousee\.com(\.br)?/?', url):
        return 'enterprise'
    elif re.match('(http:\/\/|https:\/\/)?4usee\.com\/[a-zA-Z]+\/(\w+)/?', url):
        return 'self'
    else:
        return False
