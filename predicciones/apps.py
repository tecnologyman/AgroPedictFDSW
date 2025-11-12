from django.apps import AppConfig
from django.core.management import call_command
import os

class PrediccionesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'predicciones'

    def ready(self):
        # Solo cargar si las tablas están vacías (una vez)
        from .models import TipoArbol, Comuna
        if not TipoArbol.objects.exists() or not Comuna.objects.exists():
            fixtures_path = os.path.join(os.path.dirname(__file__), 'fixtures', 'fixtures_iniciales.json')
            if os.path.exists(fixtures_path):
                try:
                    call_command('loaddata', fixtures_path)
                    print("✅ Datos iniciales cargados automáticamente.")
                except Exception as e:
                    print(f"⚠️ Error al cargar fixtures: {e}")