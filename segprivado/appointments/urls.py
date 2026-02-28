from django.urls import path

from appointments import views


urlpatterns = [
    path("especialidad/", views.DoctorsBySpecialtyView.as_view(), name="especialidad"),
    path("cita/", views.AppointmentCreateView.as_view(), name="pedirCita"),
    path("cita/indexM/", views.current_appointments, name="indexMCita"),
    path("cita/update/<int:pk>/", views.AppointmentTreatmentUpdateView.as_view(), name="actualizarCita"),
    path("cita/index/", views.patient_appointments, name="indexCita"),
    path("cita/filter/", views.PatientAppointmentFilterView.as_view(), name="filterCita"),
    path("cita/historialM/", views.doctor_history, name="historialMCita"),
    path("cita/filterP/", views.DoctorPatientFilterView.as_view(), name="filterPaciente"),
    path("api/medicos/", views.DoctorsApiView.as_view(), name="medicosAPI"),
    path("api/citas/", views.AppointmentHistoryApiView.as_view(), name="citasAPI"),
]
