import gzip
import datetime
import io
import json
from os import path
from pathlib import Path
import os
from zipfile import ZipFile

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
    Recebe o nome da aconte que vem do relatório e retorna o nome só.
    Trata e se vem com o formato 'name' ou 'name-token'
    """
    if url:
        return url.split('/')[3].split('-')[0]


def insert_records(conta, data):
    records = 0
    i = len(data) - 1
    while i:
        try:
            one_data = data[i]
            record_line = Register(nickname=one_data['account'], date=one_data['date'],
                                   time=one_data['time'], player_id=one_data['playerId'],
                                   media_id=one_data['mediaId'], media_type=one_data['type'])
            record_line.save()
            conta.register.add(record_line)
            records += 1
        except IntegrityError as e:
            pass
        i -= 1
    return records