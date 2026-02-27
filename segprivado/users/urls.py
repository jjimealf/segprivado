from django.urls import path

from users import views


urlpatterns = [
    path("registro/", views.SignupView.as_view(), name="registro"),
    path("viewProfile/", views.UserEditView.as_view(), name="viewProfile"),
]
