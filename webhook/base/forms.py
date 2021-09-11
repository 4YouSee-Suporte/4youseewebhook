from django import forms
from webhook.manager.models import Account


class RelatorioForm(forms.Form):
    """
   Este formulário vai tratar aa solicitação de relatórios.
   """
    contas = Account.objects.all()
    conta = forms.ChoiceField(choices=list(map(lambda x: (x.slug, x.name), contas)))
    startdate = forms.DateField()
    enddate = forms.DateField()
