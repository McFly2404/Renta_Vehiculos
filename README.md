# Renta de Vehículos

Este proyecto implementa una plataforma básica de alquiler de vehículos, permitiendo a los usuarios registrar reservas de acuerdo con su cédula y seleccionar vehículos disponibles por placa. El sistema gestiona la disponibilidad de vehículos y registra reservas con fechas válidas.

## Requisitos

Python 3.9 o superior  
Django 4.x  

## Instalación

1. Clonar el repositorio
2. Crear entorno virtual
3. Migrar la base de datos
4. Crear superusuario
5. Ejecutar el servidor

## Pasos

1. Clonar el repositorio:
git clone https://github.com/McFly2404/Renta_Vehiculos.git

2. Crear y activar entorno virtual:
Windows: python -m venv venv
Linux, MacOS: python3 -m venv venv

3. Migrar base de datos:
python manage.py makemigrations
python manage.py migrate

4. Crear usuario administrador:
python manage.py createsuperuser

5. Ejecutar servidor:
python manage.py runserver


## Descripción del proyecto

El proyecto fue desarrollado utilizando Django como framework principal. La intención es permitir la gestión de reservas de vehículos, usuarios y sucursales, verificando disponibilidad y aplicando reglas de negocio como validación de fechas y estado de los vehículos.

## Uso

1. Acceder a la ruta `/crear-reserva/` para crear una reserva
2. Ingresar la cédula del usuario registrado
3. Seleccionar un vehículo disponible por placa
4. Ingresar fechas de inicio y fin
5. El sistema gestiona la creación de la reserva y bloquea el vehículo

## Estructura

- `reservas/models.py`: Modelos del dominio (Usuario, Vehículo, Reserva, Pago, Contrato)
- `reservas/services.py`: Servicio de dominio para crear reserva
- `reservas/domain/reserva_builder.py`: Builder de Reserva
- `reservas/infra/notificador_factory.py`: Ejemplo de Factory para notificación
- `reservas/views.py`: Lógica de vista para crear reserva
- `templates/crear_reserva.html`: Formulario para crear reserva

## Patrones utilizados

- Builder para crear reservas y validar reglas de negocio
- Factory para desacoplar notificaciones
- Service Layer para coordinar lógica de negocio
