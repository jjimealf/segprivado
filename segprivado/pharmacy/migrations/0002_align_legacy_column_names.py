from django.db import migrations


def align_legacy_column_names(apps, schema_editor):
    connection = schema_editor.connection

    def rename_columns(table_name, rename_map):
        with connection.cursor() as cursor:
            columns = {
                column.name
                for column in connection.introspection.get_table_description(cursor, table_name)
            }

            for old_name, new_name in rename_map.items():
                if old_name in columns and new_name not in columns:
                    cursor.execute(
                        f"ALTER TABLE {table_name} RENAME COLUMN {old_name} TO {new_name}"
                    )

    rename_columns(
        "pharmacy_purchase",
        {
            "idPaciente_id": "patient_id",
        },
    )
    rename_columns(
        "pharmacy_purchaseitem",
        {
            "idCompra_id": "purchase_id",
            "idMedicamento_id": "medicine_id",
        },
    )


class Migration(migrations.Migration):
    dependencies = [
        ("pharmacy", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(align_legacy_column_names, migrations.RunPython.noop),
    ]
