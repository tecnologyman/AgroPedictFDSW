from django.db import migrations

def crear_datos_iniciales(apps, schema_editor):
    TipoArbol = apps.get_model('predicciones', 'TipoArbol')
    Comuna = apps.get_model('predicciones', 'Comuna')
    Region = apps.get_model('predicciones', 'Region')

    # Crear regiones base
    regiones = [
        ("Región Metropolitana",),
        ("Región de Valparaíso",),
        ("Región de O'Higgins",),
        ("Región del Maule",),
        ("Región de Coquimbo",),
    ]
    for (nombre,) in regiones:
        Region.objects.get_or_create(nombre=nombre)

    # Crear comunas base
    comunas = [
        ("Santiago", "Región Metropolitana"),
        ("Maipú", "Región Metropolitana"),
        ("Valparaíso", "Región de Valparaíso"),
        ("Rancagua", "Región de O'Higgins"),
        ("La Serena", "Región de Coquimbo"),
    ]
    for nombre, region_nombre in comunas:
        region = Region.objects.get(nombre=region_nombre)
        Comuna.objects.get_or_create(nombre=nombre, region=region)

    # Crear tipos de árbol base
    tipos_arbol = [
        ("Almendro", 1500, 3500, 2500, 25000, 1500000, 10, 85),
        ("Cerezo", 1200, 4000, 2800, 27000, 1300000, 9, 88),
        ("Palto", 900, 5000, 2200, 30000, 1800000, 8, 80),
        ("Naranjo", 1400, 3200, 2600, 20000, 1000000, 11, 83),
        ("Limón", 1100, 3100, 2400, 21000, 900000, 10, 81),
    ]
    for tipo, precio, costo, prod, agua, inv, edad, conf in tipos_arbol:
        TipoArbol.objects.get_or_create(
            tipo=tipo,
            defaults=dict(
                precio_promedio_ton=precio,
                costo_mantenimiento_anual=costo,
                produccion_promedio=prod,
                consumo_agua=agua,
                inversion_inicial=inv,
                edad_media=edad,
                confiabilidad_base=conf,
            )
        )

def revertir_datos(apps, schema_editor):
    TipoArbol = apps.get_model('predicciones', 'TipoArbol')
    Comuna = apps.get_model('predicciones', 'Comuna')
    Region = apps.get_model('predicciones', 'Region')
    TipoArbol.objects.all().delete()
    Comuna.objects.all().delete()
    Region.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('predicciones', '0001_initial'),  # o la última migración válida que tengas
    ]

    operations = [
        migrations.RunPython(crear_datos_iniciales, revertir_datos),
    ]
