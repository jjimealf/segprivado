from datetime import datetime

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView

from nucleo.decorators import paciente
from pharmacy.cart import Cart
from pharmacy.forms import MedicineForm, PurchaseForm
from pharmacy.models import Medicine, Purchase


@method_decorator(login_required, name="dispatch")
@method_decorator(staff_member_required, name="dispatch")
class MedicineCreateView(CreateView):
    model = Medicine
    form_class = MedicineForm
    template_name = "nucleo/medicamentos/create.html"
    success_url = reverse_lazy("nucleo:indexMedicamento")

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.form_class(request.POST)
        if form.is_valid():
            medicine = form.save(commit=False)
            medicine.save()
            messages.success(request, "Medicamento creado correctamente")
            return HttpResponseRedirect(reverse("nucleo:indexMedicamento"))
        return self.render_to_response(self.get_context_data(form=form))


@method_decorator(login_required, name="dispatch")
@method_decorator(staff_member_required, name="dispatch")
class MedicineUpdateView(UpdateView):
    model = Medicine
    form_class = MedicineForm
    template_name = "nucleo/medicamentos/create.html"
    success_url = reverse_lazy("nucleo:indexMedicamento")


@login_required
@staff_member_required
def medicine_delete(request, pk):
    medicine = get_object_or_404(Medicine, id=pk)
    medicine.delete()
    messages.success(request, "Medicamento eliminado correctamente")
    return redirect("nucleo:indexMedicamento")


@login_required
@staff_member_required
def medicine_list(request):
    medicines = Medicine.objects.all()
    return render(request, "nucleo/medicamentos/index.html", {"medicamentos": medicines})


@method_decorator(login_required, name="dispatch")
@method_decorator(paciente, name="dispatch")
class PurchaseCreateView(CreateView):
    model = Purchase
    form_class = PurchaseForm
    template_name = "nucleo/compra/create.html"
    success_url = reverse_lazy("nucleo:pedirCompra")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["medicamentos"] = Medicine.objects.all()
        context["carrito"] = self.request.session.get("carrito", {}).values()
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        Purchase.objects.create(
            patient=self.request.user,
            fecha=datetime.date(datetime.now()),
            precio=0.0,
        )
        messages.success(request, "Compra creada correctamente")
        request.session["carrito"] = {}
        return HttpResponseRedirect(reverse("nucleo:pedirCompra"))


@login_required
@paciente
def add_medicine(request, pk):
    cart = Cart(request)
    medicine = Medicine.objects.get(id=pk)
    cart.add(medicine)
    return redirect("nucleo:pedirCompra")


@login_required
@paciente
def remove_medicine(request, pk):
    cart = Cart(request)
    medicine = Medicine.objects.get(id=pk)
    cart.remove(medicine)
    return redirect("nucleo:pedirCompra")


@login_required
@paciente
def decrement_medicine(request, pk):
    cart = Cart(request)
    medicine = Medicine.objects.get(id=pk)
    cart.decrement(medicine)
    return redirect("nucleo:pedirCompra")


@login_required
@paciente
def clear_cart(request):
    cart = Cart(request)
    cart.clear()
    return redirect("nucleo:pedirCompra")
