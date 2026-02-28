from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.models import User

@login_required
def home(request):
    doctors = User.objects.filter(is_medico=True)
    return render(request, "nucleo/home.html", {"medicos": doctors})
