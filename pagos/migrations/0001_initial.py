from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True
    dependencies = [
        ("reservas", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Pago",
            fields=[
                ("id",            models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("monto",         models.DecimalField(decimal_places=2, max_digits=10)),
                ("estado_pago",   models.CharField(max_length=20, choices=[("PENDIENTE","Pendiente"),("APROBADO","Aprobado"),("RECHAZADO","Rechazado"),("REEMBOLSADO","Reembolsado")], default="PENDIENTE")),
                ("metodo_pago",   models.CharField(max_length=30, choices=[("EFECTIVO","Efectivo"),("TARJETA_CREDITO","Tarjeta de Crédito"),("TARJETA_DEBITO","Tarjeta de Débito"),("TRANSFERENCIA","Transferencia")], default="EFECTIVO")),
                ("fecha_pago",    models.DateField()),
                ("fecha_creacion",models.DateTimeField(auto_now_add=True)),
                ("reserva",       models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="pago", to="reservas.reserva")),
            ],
            options={"verbose_name": "Pago", "verbose_name_plural": "Pagos"},
        ),
    ]
