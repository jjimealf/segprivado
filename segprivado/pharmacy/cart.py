class Cart:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        cart = self.session.get("carrito")
        if not cart:
            self.session["carrito"] = {}
            self.cart = self.session["carrito"]
        else:
            self.cart = cart

    def add(self, medicine):
        medicine_id = str(medicine.id)
        available_stock = max(0, medicine.stock or 0)

        if medicine_id not in self.cart:
            if available_stock < 1:
                return False
            self.cart[medicine_id] = {
                "id": medicine.id,
                "nombre": medicine.nombre,
                "descripcion": medicine.descripcion,
                "precio": medicine.precio,
                "acumulado": medicine.precio,
                "cantidad": 1,
            }
        else:
            item = self.cart[medicine_id]
            if item["cantidad"] >= available_stock:
                return False
            item["cantidad"] += 1
            item["acumulado"] = round(item["acumulado"] + medicine.precio, 2)
        self.save()
        return True

    def save(self):
        self.session["carrito"] = self.cart
        self.session.modified = True

    def remove(self, medicine):
        medicine_id = str(medicine.id)
        if medicine_id in self.cart:
            del self.cart[medicine_id]
            self.save()

    def decrement(self, medicine):
        medicine_id = str(medicine.id)
        if medicine_id in self.cart:
            item = self.cart[medicine_id]
            item["cantidad"] -= 1
            item["acumulado"] = round(item["acumulado"] - medicine.precio, 2)
            if item["cantidad"] < 1:
                self.remove(medicine)
            else:
                self.save()

    def clear(self):
        self.session["carrito"] = {}
        self.session.modified = True

    def items(self):
        return list(self.cart.values())

    def total_quantity(self):
        return sum(int(item["cantidad"]) for item in self.cart.values())

    def total_price(self):
        return round(sum(float(item["acumulado"]) for item in self.cart.values()), 2)
