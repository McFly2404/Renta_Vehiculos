from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction

from reservas.models import Sucursal, Vehiculo


SUCURSALES = {
    "norte": {
        "nombre": "DriveNow Norte",
        "direccion": "Autopista Norte #123-45",
        "telefono": "6015550101",
        "ciudad": "Bogota",
    },
    "centro": {
        "nombre": "DriveNow Centro",
        "direccion": "Carrera 7 #32-10",
        "telefono": "6015550102",
        "ciudad": "Bogota",
    },
    "medellin": {
        "nombre": "DriveNow Medellin",
        "direccion": "Avenida El Poblado #10-20",
        "telefono": "6045550103",
        "ciudad": "Medellin",
    },
}


VEHICULOS = [
    {
        "placa": "ABC-123",
        "modelo": "Toyota Corolla 2024",
        "categoria": "SEDAN",
        "capacidad": 5,
        "color": "Blanco",
        "tarifa_diaria": Decimal("180000.00"),
        "sucursal": "norte",
    },
    {
        "placa": "DEF-456",
        "modelo": "Mazda CX-5 2023",
        "categoria": "SUV",
        "capacidad": 5,
        "color": "Gris",
        "tarifa_diaria": Decimal("260000.00"),
        "sucursal": "norte",
    },
    {
        "placa": "GHI-789",
        "modelo": "Renault Duster 2024",
        "categoria": "SUV",
        "capacidad": 5,
        "color": "Azul",
        "tarifa_diaria": Decimal("220000.00"),
        "sucursal": "centro",
    },
    {
        "placa": "JKL-012",
        "modelo": "Chevrolet Tracker 2023",
        "categoria": "SUV",
        "capacidad": 5,
        "color": "Rojo",
        "tarifa_diaria": Decimal("235000.00"),
        "sucursal": "centro",
    },
    {
        "placa": "MNO-345",
        "modelo": "Nissan Frontier 2022",
        "categoria": "CAMIONETA",
        "capacidad": 5,
        "color": "Negro",
        "tarifa_diaria": Decimal("310000.00"),
        "sucursal": "medellin",
    },
    {
        "placa": "PQR-678",
        "modelo": "Ford Ranger 2024",
        "categoria": "CAMIONETA",
        "capacidad": 5,
        "color": "Plata",
        "tarifa_diaria": Decimal("330000.00"),
        "sucursal": "medellin",
    },
    {
        "placa": "STU-901",
        "modelo": "Kia Picanto 2024",
        "categoria": "SEDAN",
        "capacidad": 4,
        "color": "Amarillo",
        "tarifa_diaria": Decimal("145000.00"),
        "sucursal": "centro",
    },
    {
        "placa": "VWX-234",
        "modelo": "BMW Serie 3 2023",
        "categoria": "DEPORTIVO",
        "capacidad": 5,
        "color": "Negro",
        "tarifa_diaria": Decimal("420000.00"),
        "sucursal": "norte",
    },
    {
        "placa": "YZA-567",
        "modelo": "Mercedes-Benz Sprinter 2022",
        "categoria": "FURGON",
        "capacidad": 12,
        "color": "Blanco",
        "tarifa_diaria": Decimal("390000.00"),
        "sucursal": "medellin",
    },
    {
        "placa": "BCD-890",
        "modelo": "Hyundai Accent 2023",
        "categoria": "SEDAN",
        "capacidad": 5,
        "color": "Gris",
        "tarifa_diaria": Decimal("165000.00"),
        "sucursal": "centro",
    },
]


class Command(BaseCommand):
    help = "Carga sucursales y vehiculos demo para no registrarlos manualmente."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset-disponibilidad",
            action="store_true",
            help="Marca los vehiculos demo como disponibles al actualizar.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        sucursales = {}
        sucursales_creadas = 0
        vehiculos_creados = 0
        vehiculos_actualizados = 0

        for key, data in SUCURSALES.items():
            sucursal, created = Sucursal.objects.update_or_create(
                nombre=data["nombre"],
                defaults={
                    "direccion": data["direccion"],
                    "telefono": data["telefono"],
                    "ciudad": data["ciudad"],
                },
            )
            sucursales[key] = sucursal
            sucursales_creadas += int(created)

        for data in VEHICULOS:
            defaults = {
                "modelo": data["modelo"],
                "categoria": data["categoria"],
                "capacidad": data["capacidad"],
                "color": data["color"],
                "tarifa_diaria": data["tarifa_diaria"],
                "sucursal": sucursales[data["sucursal"]],
            }
            if options["reset_disponibilidad"]:
                defaults["disponible"] = True

            vehiculo, created = Vehiculo.objects.update_or_create(
                placa=data["placa"],
                defaults=defaults,
            )
            vehiculo.full_clean()

            if created:
                vehiculos_creados += 1
            else:
                vehiculos_actualizados += 1

        self.stdout.write(
            self.style.SUCCESS(
                "Seed completado: "
                f"{sucursales_creadas} sucursales creadas, "
                f"{vehiculos_creados} vehiculos creados, "
                f"{vehiculos_actualizados} vehiculos actualizados."
            )
        )
