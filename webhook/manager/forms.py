import requests

from webhook.base.resources.tools import enterprise_or_self, name_of_account
from webhook.manager.models import Account
from django import forms


class ContaNovaForm(forms.ModelForm):
    """
   Este formulario va a tratar la entrada de tareas, solamente capturando su nombre.
   """

    class Meta:
        model = Account
        fields = ['url', 'token']

    # this function will be used for the validation
    def clean_url(self):

        # data from the form is fetched using super function
        super(ContaNovaForm, self).clean()

        # extract the url field from the data
        global url
        url = (lambda url: 'https://' + url if 'htt' not in url else url.replace('http', 'https'))(self.cleaned_data.get('url'))
        # conditions to be met for the url
        if '4yousee' in url or '4usee' in url:
            # self._errors['url'] = self.error_class(['Minimum 5 characters required'])
            type_account = enterprise_or_self(url)
            if type_account:
                if Account.objects.filter(url=url).exists() or Account.objects.filter(url=url + '/').exists():
                    raise forms.ValidationError("Conta existente.")
                resp = requests.get(url)
                if resp.status_code != 200:
                    raise forms.ValidationError("Não foi possível fazer contato sua conta.")
                else:
                    return url
            else:
                raise forms.ValidationError("Verifique sua URL, pode estar escrita incorretamente.")
        else:
            raise forms.ValidationError("URL inválida.")

        # return any errors if found
        # return self.cleaned_data

    def clean_token(self):
        super(ContaNovaForm, self).clean()

        # extract the url and token field from the data
        token = self.cleaned_data.get('token')

        if not token:
            raise forms.ValidationError("Este Campo é obrigatório.")
        elif len(token) < 30:
            # self._errors['token'] = self.error_class(['Post Should Contain a minimum of 10 characters'])
            raise forms.ValidationError("Token inválido.")
        else:
            resp = requests.request("GET", 'https://api.4yousee.com.br/v1/users', headers={'Secret-Token': token})
            if resp.status_code != 200:
                raise forms.ValidationError("Token inválido.")
            else:
                return token
