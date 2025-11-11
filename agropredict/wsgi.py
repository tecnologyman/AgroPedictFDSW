import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agropredict.settings')

application = get_wsgi_application()

# --- Auto-migraciones automáticas para Railway (solo demo / SQLite) ---
import django
from django.db import OperationalError
from django.core.management import call_command

django.setup()
try:
    call_command('migrate', interactive=False, run_syncdb=True)
except OperationalError:
    print("⚠️ No se pudo aplicar migraciones automáticamente (posible error de DB)")
