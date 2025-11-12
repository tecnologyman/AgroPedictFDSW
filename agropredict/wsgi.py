import os

from django.core.wsgi import get_wsgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agropredict.settings')
application = get_wsgi_application()

# 🚀 Asegurar migraciones al iniciar Railway
try:
    call_command('migrate', interactive=False)
    print("✅ Migraciones aplicadas automáticamente.")
except Exception as e:
    print(f"⚠️ No se pudieron aplicar migraciones automáticamente: {e}")
