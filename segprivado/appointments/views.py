from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from appointments.forms import AppointmentForm, AppointmentTreatmentForm
from appointments.models import Appointment
from appointments.serializers import AppointmentSerializer, DoctorSerializer
from nucleo.decorators import medico, paciente
from users.models import User


class DoctorsBySpecialtyView(ListView):
    model = User
    template_name = "nucleo/especialidad.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        specialty = self.request.GET.get("especialidad")
        if specialty and specialty != "0":
            doctors = User.objects.filter(especialidad=specialty, is_medico=True)
        else:
            doctors = User.objects.filter(is_medico=True)
        context["data"] = doctors
        return context


@method_decorator(login_required, name="dispatch")
@method_decorator(paciente, name="dispatch")
class AppointmentCreateView(CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = "nucleo/cita/create.html"
    success_url = reverse_lazy("nucleo:home")

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.form_class(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = self.request.user
            appointment.save()
            messages.success(request, "Cita creada correctamente")
            return HttpResponseRedirect(reverse("nucleo:home"))
        return self.render_to_response(self.get_context_data(form=form))


@login_required
@medico
def current_appointments(request):
    appointments = Appointment.objects.filter(
        fecha__gte=datetime.date(datetime.now()),
        doctor=request.user,
    )
    return render(request, "nucleo/cita/indexM.html", {"citas": appointments})


@method_decorator(login_required, name="dispatch")
@method_decorator(medico, name="dispatch")
class AppointmentTreatmentUpdateView(UpdateView):
    model = Appointment
    form_class = AppointmentTreatmentForm
    template_name = "nucleo/cita/update.html"
    success_url = reverse_lazy("nucleo:indexMCita")


@login_required
@paciente
def patient_appointments(request):
    appointments = Appointment.objects.filter(patient=request.user)
    return render(request, "nucleo/cita/indexP.html", {"citas": appointments})


@method_decorator(login_required, name="dispatch")
@method_decorator(paciente, name="dispatch")
class PatientAppointmentFilterView(ListView):
    model = Appointment
    template_name = "nucleo/cita/indexP.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        start_date = self.request.GET.get("fechaIni", "")
        end_date = self.request.GET.get("fechaFin", "")
        queryset = Appointment.objects.filter(
            patient=self.request.user,
            fecha__lte=datetime.date(datetime.now()),
        )
        if start_date and end_date:
            queryset = queryset.filter(fecha__range=(start_date, end_date))
        context["citas"] = queryset.order_by("fecha")
        return context


@login_required
@medico
def doctor_history(request):
    appointments = Appointment.objects.filter(
        doctor=request.user,
        fecha__lte=datetime.date(datetime.now()),
    ).order_by("fecha")
    patients = User.objects.filter(id__in=appointments.values_list("patient", flat=True).distinct())
    return render(
        request,
        "nucleo/cita/historicoM.html",
        {"citas": appointments, "pacientes": patients},
    )


@method_decorator(login_required, name="dispatch")
@method_decorator(medico, name="dispatch")
class DoctorPatientFilterView(ListView):
    model = Appointment
    template_name = "nucleo/cita/historicoM.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patient_id = self.request.GET.get("paciente", "0")
        base_queryset = Appointment.objects.filter(
            doctor=self.request.user,
            fecha__lte=datetime.date(datetime.now()),
        ).order_by("fecha")
        if patient_id != "0":
            appointments = base_queryset.filter(patient=patient_id)
            patients = User.objects.filter(id=patient_id)
        else:
            appointments = base_queryset
            patients = User.objects.filter(id__in=appointments.values_list("patient", flat=True).distinct())
        context["citas"] = appointments
        context["pacientes"] = patients
        return context


class AppointmentHistoryApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None, *args, **kwargs):
        appointments = Appointment.objects.filter(
            patient=request.user,
            fecha__lte=datetime.date(datetime.now()),
        )
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)

    def post(self, request, format=None, *args, **kwargs):
        doctor_id = request.data.get("doctor_id")
        fecha = request.data.get("fecha")
        if not doctor_id or not fecha:
            return Response({"detail": "doctor_id y fecha son obligatorios"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            doctor = User.objects.get(pk=doctor_id, is_medico=True)
        except User.DoesNotExist:
            return Response({"detail": "Medico no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        appointment = Appointment.objects.create(
            doctor=doctor,
            patient=request.user,
            fecha=fecha,
            observaciones=request.data.get("observaciones"),
        )
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DoctorsApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None, *args, **kwargs):
        appointments = Appointment.objects.filter(
            patient=request.user,
            fecha__lte=datetime.date(datetime.now()),
        ).order_by("fecha")
        doctors = User.objects.filter(id__in=appointments.values_list("doctor", flat=True).distinct())
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data)
