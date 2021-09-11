from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
import json

# Create your views here.
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from webhook.base.forms import RelatorioForm
from webhook.manager.models import Account
from webhook.base.resources.tools import *
from webhook.manager.scripts.update_data import DataManager


@csrf_exempt
def playlogs(request):
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
            return HttpResponse(f"<h4>{records} playlogs inseridos com sucesso!'</h4>")
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


@login_required
@csrf_exempt
def solicitar_relatorio(request):
    if request.method == 'POST':
        form = RelatorioForm(request.POST)
        if form.is_valid():
            slug_conta = (form.cleaned_data['conta'])
            startdate = str(form.cleaned_data['startdate'])
            enddate = str(form.cleaned_data['enddate'])
            conta = Account.objects.get(slug=slug_conta)
            account = DataManager(conta.token)
            params = dict(type='detailed', webhook=request.build_absolute_uri(reverse('base:playlogs')),
                          filter={'startDate': startdate, 'endDate': enddate,
                                  'startTime': '00:00:00', 'endTime': '23:59:59',
                                  'mediaId': [], 'playerId': [], 'sort': -1})
            resp_post = account.post_report(params)
            if resp_post.status_code != 200:
                res = json.loads(resp_post.text)
                messages.error(request, res['details']['report'][0])
                return HttpResponseRedirect(reverse('base:solicitar_relatorio'))
            else:
                messages.success(request,
                                 f"Relatório solicitado com sucesso. <a href={conta.get_absolute_url()}>Ver Playlogs</a>")
                return HttpResponseRedirect(reverse('base:solicitar_relatorio'))
        else:
            ctx = {'contas': Account.objects.all(), 'form': form}
            return render(request, 'base/solicitar_relatorio.html', ctx, status=400)


    else:
        form = RelatorioForm()
        ctx = {'contas': Account.objects.all(), 'form': form}
        return render(request, 'base/solicitar_relatorio.html', ctx)
