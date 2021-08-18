import datetime

from django import template
import itertools

from num2words import num2words

register = template.Library()


@register.filter
def group_by_day(list_all_objects):
    """
    Recebe uma lista de objetos onde cada um deles possui um atributo tipo date e logo ordena eles por dia.
    :param: list_all_objects: Register.objects.all(): django.db.models.query.QuerySet
    :return: objects_day_ordered: [[objetos_do_dia_1][objetos_do_dia_2][objetos_do_dia_3]]: list of lists
    """
    key_func = lambda x: x.date.day
    objects_day_ordered = []
    for key, group in itertools.groupby(list_all_objects, key_func):
        objects_day_ordered.insert(0, list(group))
    return objects_day_ordered


@register.filter
def num_to_word(num):
    return num2words(num)


@register.filter
def date_from_minute(m):
    """
    Calc date from minutes and return a string with the date.
    :param minutes: 351702: int
    :return: 'Jan 25 de 2021 15:44'
    """
    if m is not None:
        now = datetime.datetime.utcnow()
        deltadate = now - datetime.timedelta(minutes=m)
        return deltadate.strftime("%d %b %Y %H:%M")


@register.filter
def all_records(conta):
    qty = len(conta.categories.all()) + len(conta.players.all()) + len(conta.playlists.all()) \
          + len(conta.medias.all())
    return qty
