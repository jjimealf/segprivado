from django.urls import include, path

from nucleo import views
from users.views import ApiLoginView

app_name = "nucleo"

urlpatterns = [
    path('home', views.home, name= "home"),
    path('', include('appointments.urls')),
    path('', include('pharmacy.urls')),
    path('api/login/', ApiLoginView.as_view(), name="loginAPI"),
]
