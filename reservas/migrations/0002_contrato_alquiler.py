from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("reservas", "0001_initial"),
        ("pagos",    "0001_initial"),
        ("usuarios", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ContratoAlquiler",
            fields=[
                ("id",            models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("fecha_inicio",  models.DateField()),
                ("fecha_fin",     models.DateField()),
                ("fecha_creacion",models.DateTimeField(auto_now_add=True)),
                ("usuario",       models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="contratos", to="usuarios.usuario")),
                ("vehiculo",      models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="contratos", to="reservas.vehiculo")),
                ("pago",          models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="contrato", to="pagos.pago")),
            ],
            options={"verbose_name": "Contrato de Alquiler", "verbose_name_plural": "Contratos de Alquiler"},
        ),
    ]
