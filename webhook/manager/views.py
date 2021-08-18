from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.urls import reverse
from django.utils.text import slugify

from webhook.base.resources.inserts_to_bd import update_or_insert_players, update_or_insert_categories, \
    update_or_insert_playlists, update_or_insert_medias
from webhook.base.resources.tools import name_of_account
from webhook.manager.facade import qty_all_records
from webhook.manager.forms import ContaNovaForm
from webhook.manager.models import Account
from webhook.manager.scripts.update_data import DataManager


def home(request):
    if request.method == 'POST':
        form = ContaNovaForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.name = name_of_account(form.data['url'])
            account.slug = slugify(account.name)
            account.save()
            return HttpResponseRedirect(reverse('manager:home'))
        else:
            contas = Account.objects.all()
            return render(request, 'manager/index.html', {'form': form, 'contas': contas}, status=400)
    contas = Account.objects.all()
    return render(request, 'manager/index.html', {'contas': contas})


def conta(request, slug):
    conta = get_object_or_404(Account, slug=slug)
    ctx = {'conta': conta, 'total_records': qty_all_records(conta)}
    return render(request, 'manager/conta.html', ctx)


def update_all_data_account(request, slug):
    conta = Account.objects.get(slug=slug)
    account = DataManager(conta.token)
    account.get_media_category(), account.get_medias(), account.get_playlists(), account.get_players()
    msg = ''
    if not account.media_category:
        msg += "• Não foi possível capturar informações das categorias."
    else:
        update_or_insert_categories(conta, account.media_category)

    if not account.medias:
        msg += "\n• Não foi possível capturar informações dos conteúdos."
    else:
        update_or_insert_medias(conta, account.medias)

    if not account.playlists:
        msg += "\n• Não foi possível capturar informações das playlists e por causa disso não podem ser obtidos os dados dos players."
    elif not account.players:
        update_or_insert_playlists(conta, account.playlists)
        msg += "\n• Não foi possível capturar informações dos players."
    else:
        update_or_insert_playlists(conta, account.playlists)
        update_or_insert_players(conta, account.players)

    messages.error(request, msg)
    return redirect(
        conta)  # By passing some object to redirect(); that object’s get_absolute_url() method will be called to figure out the redirect URL


def update_players(request, slug):
    conta = Account.objects.get(slug=slug)
    account = DataManager(conta.token)
    account.get_players()
    if not account.players:
        messages.error(request, "Não foi possível capturar informações dos players.")
        return redirect(conta)
    else:
        records = update_or_insert_players(conta, account.players)
        if records:
            return redirect(conta)
        else:
            messages.error(request, "Não foi possível capturar informações dos players.")
            return redirect(conta)


def update_categories(request, slug):
    conta = Account.objects.get(slug=slug)
    account = DataManager(conta.token)
    account.get_media_category()
    if not account.media_category:
        messages.error(request, "Não foi possível capturar informações das categorias")
        return redirect(conta)
    else:
        update_or_insert_categories(conta, account.media_category)
        return redirect(conta)


def update_playlists(request, slug):
    conta = Account.objects.get(slug=slug)
    account = DataManager(conta.token)
    account.get_playlists()
    if not account.playlists:
        messages.error(request, "Não foi possível capturar informações das playlists")
        return redirect(conta)
    else:
        update_or_insert_playlists(conta, account.playlists)
        return redirect(conta)


def update_medias(request, slug):
    conta = Account.objects.get(slug=slug)
    account = DataManager(conta.token)
    account.get_medias()
    if not account.medias:
        messages.error(request, "Não foi possível capturar informações dos conteúdos")
        return redirect(conta)
    else:
        update_or_insert_medias(conta, account.medias)
        return redirect(conta)


def delete(request, slug):
    conta = Account.objects.get(slug=slug)
    conta.delete()
    return HttpResponseRedirect(reverse('manager:home'))
