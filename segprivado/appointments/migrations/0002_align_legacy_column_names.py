from django.db import migrations


def align_legacy_column_names(apps, schema_editor):
    table_name = "appointments_appointment"
    connection = schema_editor.connection

    with connection.cursor() as cursor:
        columns = {
            column.name
            for column in connection.introspection.get_table_description(cursor, table_name)
        }

        if "idMedico_id" in columns and "doctor_id" not in columns:
            cursor.execute(
                "ALTER TABLE appointments_appointment RENAME COLUMN idMedico_id TO doctor_id"
            )

        if "idPaciente_id" in columns and "patient_id" not in columns:
            cursor.execute(
                "ALTER TABLE appointments_appointment RENAME COLUMN idPaciente_id TO patient_id"
            )


class Migration(migrations.Migration):
    dependencies = [
        ("appointments", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(align_legacy_column_names, migrations.RunPython.noop),
    ]
