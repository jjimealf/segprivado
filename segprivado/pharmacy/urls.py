from django.urls import path

from pharmacy import views


urlpatterns = [
    path("medicamento/", views.medicine_list, name="indexMedicamento"),
    path("medicamento/create/", views.MedicineCreateView.as_view(), name="crearMedicamento"),
    path("medicamento/update/<int:pk>/", views.MedicineUpdateView.as_view(), name="actualizarMedicamento"),
    path("medicamento/delete/<int:pk>/", views.medicine_delete, name="eliminarMedicamento"),
    path("compra/", views.PurchaseCreateView.as_view(), name="pedirCompra"),
    path("compra/add/<int:pk>/", views.add_medicine, name="addMedicamento"),
    path("compra/remove/<int:pk>/", views.remove_medicine, name="removeMedicamento"),
    path("compra/subtract/<int:pk>/", views.decrement_medicine, name="restarMedicamento"),
    path("compra/clear/", views.clear_cart, name="limpiarCarrito"),
]
