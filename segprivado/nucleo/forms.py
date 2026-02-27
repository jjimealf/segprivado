from appointments.forms import AppointmentForm, AppointmentTreatmentForm
from appointments.models import Appointment
from pharmacy.forms import MedicineForm, PurchaseForm
from pharmacy.models import Medicine, Purchase
from users.models import User


Usuario = User
Cita = Appointment
Medicamento = Medicine
Compra = Purchase

citaForm = AppointmentForm
citaFormTratamiento = AppointmentTreatmentForm
medicamentoForm = MedicineForm
compraForm = PurchaseForm
