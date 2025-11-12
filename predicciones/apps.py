from django.apps import AppConfig
from django.core.management import call_command
from django.db.utils import OperationalError, ProgrammingError
import os

class PrediccionesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'predicciones'

    def ready(self):
        from django.db import connection
        try:
            tables = connection.introspection.table_names()
            if 'predicciones_tipoarbol' in tables and 'predicciones_comuna' in tables:
                from .models import TipoArbol, Comuna
                if not TipoArbol.objects.exists() or not Comuna.objects.exists():
                    fixtures_path = os.path.join(os.path.dirname(__file__), 'fixtures', 'fixtures_iniciales.json')
                    if os.path.exists(fixtures_path):
                        call_command('loaddata', fixtures_path)
                        print("✅ Datos iniciales cargados automáticamente.")
        except (OperationalError, ProgrammingError):
            print("⏳ Migraciones aún no listas, omitiendo carga inicial.")
