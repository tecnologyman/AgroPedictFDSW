from django.apps import AppConfig
from django.core.management import call_command
from django.db.utils import OperationalError, ProgrammingError
import os

class PrediccionesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'predicciones'

    def ready(self):
        """
        Carga fixtures iniciales automáticamente en Railway,
        pero solo si las migraciones ya existen y las tablas están creadas.
        """
        try:
            from .models import TipoArbol, Comuna

            # Verifica si las tablas existen realmente
            from django.db import connection
            tables = connection.introspection.table_names()
            if 'predicciones_tipoarbol' not in tables or 'predicciones_comuna' not in tables:
                print("⏳ Tablas aún no creadas. Se omitió carga inicial.")
                return

            # Carga solo si están vacías
            if not TipoArbol.objects.exists() or not Comuna.objects.exists():
                fixtures_path = os.path.join(os.path.dirname(__file__), 'fixtures', 'fixtures_iniciales.json')
                if os.path.exists(fixtures_path):
                    call_command('loaddata', fixtures_path)
                    print("✅ Datos iniciales cargados automáticamente.")
                else:
                    print("⚠️ No se encontró fixtures_iniciales.json.")
        except (OperationalError, ProgrammingError):
            # Esto ocurre si aún no se aplicaron migraciones
            print("⚠️ No se pudo acceder a la base de datos. Las migraciones pueden no estar aplicadas todavía.")
        except Exception as e:
            print(f"⚠️ Error inesperado al cargar fixtures: {e}")
