from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from nucleo.models import Usuario
from nucleo.forms import *
from django.views.generic import CreateView, UpdateView, ListView
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from nucleo.decorators import *
from nucleo.serializers import citaSerializer, medicoSerializer
from .carrito import Carrito

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework import serializers, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
# Create your views here.

@login_required
def home(request):
    medico=Usuario.objects.filter(is_medico=True)
    
    
    context={'medicos':medico,
 }
    return render(request, 'nucleo/home.html')

@method_decorator(login_required, name='dispatch')
@method_decorator(staff_member_required, name='dispatch')
class medicamentoCreate(CreateView):
      model = Medicamento
      form_class = medicamentoForm
      template_name = 'nucleo/medicamentos/create.html'
      success_url = reverse_lazy('nucleo:indexMedicamento')

      def post(self, request, *args, **kwargs):
         self.object = self.get_object
         form = self.form_class(request.POST)
         if form.is_valid():
            medicamento = form.save(commit=False)
            medicamento.save()
            messages.success(request, 'Medicamento creado correctamente')
            return HttpResponseRedirect(reverse('nucleo:indexMedicamento'))
         else:
            return self.render_to_response(self.get_context_data(form=form))

@method_decorator(login_required, name='dispatch')
@method_decorator(staff_member_required, name='dispatch')
class medicamentoUpdate(UpdateView):
      model = Medicamento
      form_class = medicamentoForm
      template_name = 'nucleo/medicamentos/create.html'
      success_url = reverse_lazy('nucleo:indexMedicamento')

@login_required
@staff_member_required
def medicamentoDelete(request, pk):
   medicamento = get_object_or_404(Medicamento, id=pk)
   medicamento.delete()
   messages.success(request, 'Medicamento eliminado correctamente')
   return redirect('nucleo:indexMedicamento')

@login_required
@staff_member_required
def medicamento(request):
   medicamentos = Medicamento.objects.all()
   context = {'medicamentos': medicamentos}
   return render(request, 'nucleo/medicamentos/index.html', context)

class medicosEspecilidad(ListView):
   model = Usuario
   template_name = 'nucleo/especialidad.html'

   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      especialidadGet = self.request.GET.get('especialidad')
      
      if(self.request.GET.get('especialidad')!=0):
         data = Usuario.objects.filter(especialidad=especialidadGet, is_medico=True)
      else:
         data = Usuario.objects.filter(is_medico=True)
      
      context['data'] = data
      return context

@method_decorator(login_required, name='dispatch')
@method_decorator(paciente, name='dispatch')
class createCita(CreateView):
   model = Cita
   form_class = citaForm
   template_name = 'nucleo/cita/create.html'
   success_url = reverse_lazy('nucleo:home')

   def post(self, request, *args, **kwargs):
      self.object = self.get_object
      form = self.form_class(request.POST)
      if form.is_valid():
         cita = form.save(commit=False)
         cita.idPaciente = self.request.user
         cita.idMedico = form.cleaned_data['idMedico']
         cita.save()
         messages.success(request, 'Cita creada correctamente')
         return HttpResponseRedirect(reverse('nucleo:home'))
      else:
         return self.render_to_response(self.get_context_data(form=form))
   
   def dispatch(self, request, *args, **kwargs):
         return super().dispatch(request, *args, **kwargs)

@login_required
@medico
def citasActual(request):
   citas = Cita.objects.filter(fecha__gte=datetime.date(datetime.now()), idMedico=request.user.id)
   context = {'citas': citas}
   return render(request, 'nucleo/cita/indexM.html', context)

@method_decorator(login_required, name='dispatch')
@method_decorator(medico, name='dispatch')
class citaTratamiento(UpdateView):
   model = Cita
   form_class = citaFormTratamiento
   template_name = 'nucleo/cita/update.html'
   success_url = reverse_lazy('nucleo:actualizarCita')

@login_required
@paciente
def verCitas(request):
   if(request.user.is_paciente):
      citas = Cita.objects.filter(idPaciente=request.user.id)
   context = {'citas': citas}
   return render(request, 'nucleo/cita/indexP.html', context)

@method_decorator(login_required, name='dispatch')
@method_decorator(paciente, name='dispatch')
class citasFilter(ListView):
   model = Cita
   template_name = 'nucleo/cita/indexP.html'

   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      fechaIni = self.request.GET.get('fechaIni', None)
      fechaFin = self.request.GET.get('fechaFin', None)
      if fechaIni != '' and fechaFin != '':
         citas = Cita.objects.filter(idPaciente=self.request.user.id, fecha__range=(fechaIni, fechaFin)).filter(fecha__lte=datetime.date(datetime.now())).order_by('fecha')
      else:
         citas = Cita.objects.filter(idPaciente=self.request.user.id).filter(fecha__lte=datetime.date(datetime.now())).order_by('fecha')
      context['citas'] = citas
      return context

@login_required
@medico
def verCitasMedico(request):
   if(request.user.is_medico):
      citas = Cita.objects.filter(idMedico=request.user.id, fecha__lte=datetime.date(datetime.now())).order_by('fecha')
      paciente = citas.values_list('idPaciente', flat=True).distinct()
      pacientes = Usuario.objects.filter(id__in=paciente)
   context = {'citas': citas, 'pacientes': pacientes}
   return render(request, 'nucleo/cita/historicoM.html', context)

@method_decorator(login_required, name='dispatch')
@method_decorator(medico, name='dispatch')
class filterPaciente(ListView):
   model = Cita
   template_name = 'nucleo/cita/historicoM.html'

   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      paciente = self.request.GET.get('paciente', None)
      pacientes = Usuario.objects.filter(id__in=paciente)
      if paciente != '0':
         citas = Cita.objects.filter(idMedico=self.request.user.id, idPaciente=paciente, fecha__lte=datetime.date(datetime.now())).order_by('fecha')
      else:
         citas = Cita.objects.filter(idMedico=self.request.user.id, fecha__lte=datetime.date(datetime.now())).order_by('fecha')
         pacientes = Usuario.objects.filter(id__in=citas.values_list('idPaciente', flat=True).distinct())
      context['citas'] = citas
      context['pacientes'] = pacientes
      return context

@method_decorator(login_required, name='dispatch')
@method_decorator(paciente, name='dispatch')
class createCompra(CreateView):
   model = Compra
   form_class = compraForm
   template_name = 'nucleo/compra/create.html'
   success_url = reverse_lazy('nucleo:pedirCompra')
   medicamentos = Medicamento.objects.all()
   
   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['medicamentos'] = self.medicamentos
      return context

   def post(self, request, *args, **kwargs):
      self.object = self.get_object
      form = self.form_class(request.POST)
      if form.is_valid():
         compra = form.save(commit=False)
         compra.idPaciente = self.request.user
         compra.save()
         messages.success(request, 'Compra creada correctamente')
         return HttpResponseRedirect(reverse('nucleo:pedirCompra'))
      else:
         return self.render_to_response(self.get_context_data(form=form))
   
   def addMedicamento(request,pk):
      carrito = Carrito(request)
      medicamento = Medicamento.objects.get(id=pk)
      carrito.agregar(medicamento)
      return redirect('nucleo:pedirCompra')

   def removeMedicamento(request,pk):
      carrito = Carrito(request)
      medicamento = Medicamento.objects.get(id=pk)
      carrito.eliminar(medicamento=medicamento)
      return redirect('nucleo:pedirCompra')

   def restarMedicamento(request,pk):
      carrito = Carrito(request)
      medicamento = Medicamento.objects.get(id=pk)
      carrito.restar(medicamento=medicamento)
      return redirect('nucleo:pedirCompra')

   def limpiarCarrito(request):
      carrito = Carrito(request)
      carrito.limpiar()
      return redirect('nucleo:pedirCompra')

class loginAPI(APIView):
   def get(self, request, format=None):
      return Response({'detail':'GET Response'})

   def post(self, request, format=None):
      try:
         data=request.data
      except ParseError as error:
         return Response(
            'INVALID JSON - {0}'.format(error.detail),
            status=status.HTTP_400_BAD_REQUEST
         )
      if "user" not in data or "password" not in data:
         return Response(
            'Credenciales incorrectas',
            status=status.HTTP_401_UNAUTHORIZED
         )
      
      user = Usuario.objects.get(username=data["user"])

      if not user:
         return Response(
            'Usuario no encontrado',
            status=status.HTTP_404_NOT_FOUND
         )
      if user.is_paciente == False or user.is_active == False:
         return Response(
            'Usuario no autorizado',
            status=status.HTTP_404_NOT_FOUND
         )
      if check_password(data["password"], user.password)==False:
         return Response(
            'Credenciales incorrectas',
            status=status.HTTP_404_NOT_FOUND
         )
      token = Token.objects.get_or_create(user=user)

      return Response({'token': token[0].key})

class  historialCitas_APIView(APIView):
   permission_classes = [IsAuthenticated]     
   def get(self, request, format=None, *args, **kwargs):
      citas = Cita.objects.filter(idPaciente=request.user.id, fecha__lte=datetime.date(datetime.now()))
      serializer = citaSerializer(citas, many=True)
      return Response(serializer.data)
   
   def post(self, request, format=None, *args, **kwargs):
      serializer = citaSerializer(data=request.data)
      if serializer.is_valid():
         serializer.save()
         return Response(serializer.data, status=status.HTTP_201_CREATED)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class medicos_APIView(APIView):
   permission_classes = [IsAuthenticated]     
   def get(self, request, format=None, *args, **kwargs):
      citas = Cita.objects.filter(idPaciente=request.user.id, fecha__lte=datetime.date(datetime.now())).order_by('fecha')
      medicos = Usuario.objects.filter(id__in=citas.values_list('idMedico', flat=True).distinct())
      serializer = medicoSerializer(medicos, many=True)
      return Response(serializer.data)
