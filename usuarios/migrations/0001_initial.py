from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Usuario",
            fields=[
                ("id",       models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nombre",   models.CharField(max_length=100)),
                ("cedula",   models.CharField(max_length=20, unique=True)),
                ("correo",   models.EmailField(max_length=254, unique=True)),
                ("licencia", models.CharField(max_length=50, unique=True)),
            ],
            options={"verbose_name": "Usuario", "verbose_name_plural": "Usuarios"},
        ),
    ]
