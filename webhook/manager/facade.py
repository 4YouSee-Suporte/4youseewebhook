from typing import List

from webhook.manager.models import Account


def listar_contas() -> List[Account]:
    """
    Lista contas por date_added.
    """
    return list(Account.objects.order_by('name').all())


def qty_all_records(conta):
    """
    Quantidade total de registros que uma conta possui.
    """
    qty = len(conta.categories.all()) + len(conta.players.all()) + len(conta.playlists.all()) \
          + len(conta.playlists.all())
    return qty
