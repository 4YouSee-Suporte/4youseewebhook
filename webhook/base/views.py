from django.http import HttpResponse
from django.shortcuts import render
import json

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from webhook.base.models import Account
from webhook.base.resources.tools import download_gz, process_file, bytes_to_dict, name_of_account, insert_records


@csrf_exempt
def home(request):
    data = None
    if request.method == 'POST':
        content = bytes_to_dict(request.body)
        data_response = json.dumps(content, indent=2)
        print(data_response)
        file = download_gz(content['url'])
        data = process_file(file)
        if data:
            name_account = name_of_account(content['url'])
            try:
                # Se a conta consultada existe no banco a atribuição não da erro
                conta = Account.objects.get(name__contains=name_account)
                records = insert_records(conta, data)
            except Account.DoesNotExist:
                # se a conta não existe, é criado um registro de conta no bd
                conta = Account.objects.create(name=name_account.capitalize())
                records = insert_records(conta, data)
            except Exception as e:
                print('Error: ', e)
            return HttpResponse(
                f'{records} Registros inseridos com sucesso! na conta {conta.name}')
        else:
            return HttpResponse(
                f"Conta: {name_of_account(content['url']).capitalize()}\n"
                f"Sem dados no intervalo :\n\t{content['filter']['startDate']} - {content['filter']['endDate']}"
                f"\n\t{content['filter']['startTime']} - {content['filter']['endTime']}\n\tPlayers: {content['filter']['playerId']}\n\tConteúdos: {content['filter']['mediaId']}")
    else:
        # print(request.__dict__)
        return render(request, 'base/index.html', context={'lines': data})
