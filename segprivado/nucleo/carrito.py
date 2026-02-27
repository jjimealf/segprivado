class Carrito:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        carrito = self.session.get("carrito")
        if not carrito:
            self.session["carrito"] = {}
            self.carrito = self.session["carrito"]
        else:
            self.carrito = carrito

    def agregar(self, medicamento):
        id = str(medicamento.id)
        if id not in self.carrito.keys():
            self.carrito[id]={
                "id": medicamento.id,
                "nombre": medicamento.nombre,
                "acumulado": medicamento.precio,
                "cantidad": 1,
            }
        else:
            for key, value in self.carrito.items():
                if key == id:
                    value["cantidad"] = value["cantidad"] + 1
                    value["acumulado"] = value["acumulado"] + medicamento.precio
                    break
        self.save()
           
    def save(self):
        self.session["carrito"] = self.carrito
        self.session.modified = True

    def eliminar(self, medicamento):
        id = str(medicamento.id)
        if id in self.carrito:
            del self.carrito[id]
            self.save()

    def restar(self, medicamento):
        id = str(medicamento.id)
        for key, value in self.carrito.items():
                if key == id:
                    value["cantidad"] = value["cantidad"] - 1
                    value["acumulado"] = value["acumulado"] + medicamento.precio
                    if value["cantidad"] < 1:
                        self.eliminar(medicamento)
                    break
        self.save()

    def limpiar(self):
        self.session["carrito"] = {}
        self.session.modified = True