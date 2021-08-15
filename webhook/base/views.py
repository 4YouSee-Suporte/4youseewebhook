from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
import json

# Create your views here.
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from webhook.manager.models import Account
from webhook.base.resources.tools import *


@csrf_exempt
def home(request):
    data = None
    if request.method == 'POST':
        content = bytes_to_dict(request.body)
        data_response = json.dumps(content, indent=2)
        print(content)
        file = download_gz(content['url'])
        data = process_file(file)
        if data:
            name_account = name_of_account(content['url'])
            try:
                conta = Account.objects.get(name__contains=name_account.split('-')[0].capitalize())
                records = insert_records(conta, data)
            except Exception as e:
                print('Error: ', e)
            return HttpResponse(reverse('base:home'))
        else:
            return render(request, 'base/playlogs.html', context={'contas': Account.objects.all(),
                                                                  'no_info': {
                                                                      'conta': name_of_account(
                                                                          content['url']).capitalize(),
                                                                      'interval_date': f"{content['filter']['startDate']} - {content['filter']['endDate']}",
                                                                      'interval_time': f"{content['filter']['startTime']} - {content['filter']['endTime']}",
                                                                      'players': content['filter']['playerId'],
                                                                      'medias': content['filter']['mediaId']
                                                                  }
                                                                  }
                          )
    return render(request, 'base/playlogs.html', context={'contas': Account.objects.all(), })
