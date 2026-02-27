from django.contrib import admin
from django.urls import path
from django.views.generic.base import TemplateView
from registration import views

urlpatterns = [
   
   
   path('registro/', views.SignupView.as_view(), name="registro"),
   path('viewProfile/', views.UserEditView.as_view(), name="viewProfile"),

   path('especialidad/', views.medicosEspecilidad.as_view(), name="especialidad"),
]