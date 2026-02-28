from datetime import datetime

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView

from nucleo.decorators import paciente
from pharmacy.cart import Cart
from pharmacy.forms import MedicineForm, PurchaseForm
from pharmacy.models import Medicine, Purchase, PurchaseItem


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
        cart = Cart(self.request)
        cart_items = cart.items()
        context["medicamentos"] = Medicine.objects.all()
        context["carrito"] = cart_items
        context["cart_lookup"] = {item["id"]: item for item in cart_items}
        context["cart_lines"] = len(cart_items)
        context["cart_units"] = cart.total_quantity()
        context["cart_total"] = cart.total_price()
        context["purchase_date"] = datetime.date(datetime.now())
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        cart = Cart(request)
        cart_items = cart.items()

        if not cart_items:
            messages.error(request, "El carrito esta vacio")
            return HttpResponseRedirect(reverse("nucleo:pedirCompra"))

        medicine_ids = [item["id"] for item in cart_items]

        with transaction.atomic():
            medicines = {
                medicine.id: medicine
                for medicine in Medicine.objects.select_for_update().filter(id__in=medicine_ids)
            }
            purchase_lines = []
            total = 0.0

            for item in cart_items:
                medicine = medicines.get(item["id"])
                if medicine is None:
                    messages.error(request, "Uno de los medicamentos ya no esta disponible")
                    return HttpResponseRedirect(reverse("nucleo:pedirCompra"))

                quantity = int(item["cantidad"])
                available_stock = max(0, medicine.stock or 0)

                if quantity > available_stock:
                    messages.error(
                        request,
                        f"No hay stock suficiente para {medicine.nombre}. Disponible: {available_stock}",
                    )
                    return HttpResponseRedirect(reverse("nucleo:pedirCompra"))

                unit_price = float(medicine.precio or 0)
                line_total = round(unit_price * quantity, 2)
                total += line_total
                purchase_lines.append((medicine, quantity))

            purchase = Purchase.objects.create(
                patient=self.request.user,
                fecha=datetime.date(datetime.now()),
                precio=round(total, 2),
            )

            for medicine, quantity in purchase_lines:
                PurchaseItem.objects.create(
                    purchase=purchase,
                    medicine=medicine,
                    cant=quantity,
                )
                medicine.stock = max(0, (medicine.stock or 0) - quantity)
                medicine.save(update_fields=["stock"])

        messages.success(request, "Compra creada correctamente")
        cart.clear()
        return HttpResponseRedirect(reverse("nucleo:pedirCompra"))


@login_required
@paciente
def add_medicine(request, pk):
    cart = Cart(request)
    medicine = get_object_or_404(Medicine, id=pk)
    if not cart.add(medicine):
        messages.warning(request, f"No puedes agregar mas unidades de {medicine.nombre}")
    return redirect("nucleo:pedirCompra")


@login_required
@paciente
def remove_medicine(request, pk):
    cart = Cart(request)
    medicine = get_object_or_404(Medicine, id=pk)
    cart.remove(medicine)
    return redirect("nucleo:pedirCompra")


@login_required
@paciente
def decrement_medicine(request, pk):
    cart = Cart(request)
    medicine = get_object_or_404(Medicine, id=pk)
    cart.decrement(medicine)
    return redirect("nucleo:pedirCompra")


@login_required
@paciente
def clear_cart(request):
    cart = Cart(request)
    cart.clear()
    return redirect("nucleo:pedirCompra")


@login_required
@paciente
def purchase_history(request):
    purchases = (
        Purchase.objects.filter(patient=request.user)
        .prefetch_related("purchaseitem_set__medicine")
        .order_by("-fecha", "-id")
    )
    return render(request, "nucleo/compra/history.html", {"purchases": purchases})
