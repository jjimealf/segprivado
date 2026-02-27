from django.urls import path
from nucleo import views

app_name = "nucleo"

urlpatterns = [
    
    path('home', views.home, name= "home"),

    path('medicamento/', views.medicamento, name="indexMedicamento"),
    path('medicamento/create/', views.medicamentoCreate.as_view(), name="crearMedicamento"),
    path('medicamento/update/<int:pk>/', views.medicamentoUpdate.as_view(), name="actualizarMedicamento"),
    path('medicamento/delete/<int:pk>/', views.medicamentoDelete, name="eliminarMedicamento"),

    path('especialidad/', views.medicosEspecilidad.as_view(), name="especialidad"),

    path('cita/', views.createCita.as_view(), name="pedirCita"),
    path('cita/indexM/', views.citasActual, name="indexMCita"),
    path('cita/update/<int:pk>/', views.citaTratamiento.as_view(), name="actualizarCita"),
    path('cita/index/', views.verCitas, name="indexCita"),
    path('cita/filter/', views.citasFilter.as_view(), name="filterCita"),
    path('cita/historialM/', views.verCitasMedico, name="historialMCita"),
    path('cita/filterP/', views.filterPaciente.as_view(), name="filterPaciente"),

    path('compra/', views.createCompra.as_view(), name="pedirCompra"),
    path('compra/add/<int:pk>/', views.createCompra.addMedicamento, name="addMedicamento"),

    path('api/login/', views.loginAPI.as_view(), name="loginAPI"),
    path('api/medicos/', views.medicos_APIView.as_view(), name="medicosAPI"),
    path('api/citas/', views.historialCitas_APIView.as_view(), name="citasAPI"),
]