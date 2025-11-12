from django.db import migrations
import os


def create_default_admin(apps, schema_editor):
    """Crea un superusuario por defecto si no existe."""
    from django.contrib.auth import get_user_model
    User = get_user_model()

    username = os.getenv("DJANGO_ADMIN_USER", "tecnologyman")
    email = os.getenv("DJANGO_ADMIN_EMAIL", "tecnologyman@agropredict.cl")
    password = os.getenv("DJANGO_ADMIN_PASS", "Matiasaguayo13!")

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)
        print(f"✅ Superusuario '{username}' creado correctamente.")
    else:
        print("ℹ️ Superusuario ya existe, no se crea uno nuevo.")


class Migration(migrations.Migration):
    dependencies = [
        ('predicciones', '0005_alter_prediccionlstm_rendimiento_predicho_ano_actual'),  # cambia por tu última migración real
    ]

    operations = [
        migrations.RunPython(create_default_admin),
    ]
