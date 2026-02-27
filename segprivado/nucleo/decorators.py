from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect

from nucleo.models import Usuario


def paciente(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='home'):
   
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_paciente,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def medico(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='home'):
   
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_medico,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def same_user(func):
    def check_and_call(request, *args, kwargs):
        pk = kwargs['pk']
        user = Usuario.objects.get(pk=pk)

        if not request.user.is_staff:
            if not (user.id == request.user.id):
                
                if request.user.is_paciente == True:
                    return HttpResponseRedirect('/')
                elif request.user.is_medico == True:
                    return HttpResponseRedirect('/')

        return func(request, *args, kwargs)

    return check_and_call