from django.http import HttpResponse


def home(request):
    return HttpResponse('Página para uso exclusivo de 4YouSee')