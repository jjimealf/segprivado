from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from users.models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = DjangoUserAdmin.fieldsets + (
        (
            "Perfil",
            {
                "fields": (
                    "edad",
                    "especialidad",
                    "is_paciente",
                    "is_medico",
                    "direccion",
                    "foto",
                )
            },
        ),
    )

    add_fieldsets = DjangoUserAdmin.add_fieldsets + (
        (
            "Perfil",
            {
                "fields": (
                    "email",
                    "edad",
                    "especialidad",
                    "is_paciente",
                    "is_medico",
                    "direccion",
                )
            },
        ),
    )
