from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True
    dependencies = [
        ("usuarios", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Sucursal",
            fields=[
                ("id",        models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nombre",    models.CharField(max_length=100)),
                ("direccion", models.CharField(max_length=200)),
                ("telefono",  models.CharField(max_length=20)),
                ("ciudad",    models.CharField(max_length=100)),
            ],
            options={"verbose_name": "Sucursal", "verbose_name_plural": "Sucursales"},
        ),
        migrations.CreateModel(
            name="Vehiculo",
            fields=[
                ("id",           models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("placa",        models.CharField(max_length=20, unique=True)),
                ("modelo",       models.CharField(max_length=50)),
                ("categoria",    models.CharField(max_length=50, choices=[("SEDAN","Sedán"),("SUV","SUV"),("CAMIONETA","Camioneta"),("DEPORTIVO","Deportivo"),("FURGON","Furgón")])),
                ("capacidad",    models.PositiveIntegerField()),
                ("color",        models.CharField(max_length=30)),
                ("tarifa_diaria",models.DecimalField(decimal_places=2, max_digits=10)),
                ("disponible",   models.BooleanField(default=True)),
                ("sucursal",     models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="vehiculos", to="reservas.sucursal")),
            ],
            options={"verbose_name": "Vehículo", "verbose_name_plural": "Vehículos"},
        ),
        migrations.CreateModel(
            name="Reserva",
            fields=[
                ("id",            models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("fecha_inicio",  models.DateField()),
                ("fecha_fin",     models.DateField()),
                ("estado",        models.CharField(max_length=20, choices=[("PENDIENTE","Pendiente"),("CONFIRMADA","Confirmada"),("CANCELADA","Cancelada"),("COMPLETADA","Completada")], default="PENDIENTE")),
                ("fecha_creacion",models.DateTimeField(auto_now_add=True)),
                ("usuario",       models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="reservas", to="usuarios.usuario")),
                ("vehiculo",      models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="reservas", to="reservas.vehiculo")),
            ],
            options={"verbose_name": "Reserva", "verbose_name_plural": "Reservas"},
        ),
    ]
