from django.db import migrations

def create_categories(apps, schema_editor):
    Category = apps.get_model('ecommerce', 'Category')
    
    categories_data = [
        ('Joyeria', [
            'Joyeria de Plata',
            'Joyería Artesanal',
            'Collares Típicos',
            'Pulseras de Hilo',
            'Arte en Jícaras'
        ]),
        ('Muebles', [
            'Muebles de Madera',
            'Muebles Típicos',
            'Muebles de Bambú',
            'Muebles Minimalistas',
            'Muebles Infantiles'
        ]),
        ('Tiendas', [
            'Tiendas de Barrio',
            'Minisúpers',
            'Tiendas Orgánicas',
            'Tiendas de Artesanías',
            'Tiendas de Conveniencia'
        ]),
        ('Belleza', [
            'Productos Naturales',
            'Cosméticos Artesanales',
            'Cuidado Capilar',
            'Maquillaje',
            'Perfumería'
        ]),
        ('Ropa', [
            'Ropa Tradicional',
            'Vestidos Típicos',
            'Ropa Casual',
            'Ropa Deportiva',
            'Ropa para Bebés'
        ]),
        ('Juguetes', [
            'Juguetes Educativos',
            'Juguetes de Madera',
            'Juguetes Típicos',
            'Muñecas Artesanales',
            'Juegos al Aire Libre'
        ]),
        ('Bebés', [
            'Pañales Ecológicos',
            'Ropa para Bebés',
            'Cuidado del Bebé',
            'Juguetes para Bebés',
            'Portabebés Artesanales'
        ]),
        ('Librería', [
            'Libros en Español',
            'Literatura Salvadoreña',
            'Material Educativo',
            'Libros Infantiles',
            'Arte y Diseño'
        ]),
        ('Deportes', [
            'Equipo de Fútbol',
            'Ropa Deportiva',
            'Artículos para Surf',
            'Yoga y Pilates',
            'Ciclismo'
        ]),
        ('Viajes', [
            'Turismo Local',
            'Tours Culturales',
            'Artesanías de Viaje',
            'Equipaje',
            'Guías Turísticas'
        ]),
        ('Mascotas', [
            'Alimento para Mascotas',
            'Juguetes para Mascotas',
            'Ropa para Mascotas',
            'Cuidado Veterinario',
            'Accesorios'
        ]),
        ('Salud y Belleza', [
            'Productos Naturales',
            'Medicinas Alternativas',
            'Cosméticos Artesanales',
            'Equipo Médico Básico',
            'Aceites Esenciales',
            'Suplementos',
            'Remedios Naturales',
            'Cuidado Personal'
        ]),
        # Salvadoran-specific categories
        ('Artesanías Salvadoreñas', [
            'Hamacas de San Sebastián',
            'Cerámica de Ilobasco',
            'Jícaras Pintadas',
            'Textiles de Nahuizalco',
            'Souvenirs Típicos'
        ]),
        ('Comida Típica', [
            'Pupuserías',
            'Productos de Maíz',
            'Dulces Tradicionales',
            'Café Salvadoreño',
            'Conservas Artesanales'
        ]),
        ('Alimentos y Bebidas', [
            'Comida Típica Salvadoreña',
            'Pupuserías',
            'Panadería Tradicional',
            'Café Salvadoreño',
            'Productos Orgánicos'
        ]),
        ('Moda y Accesorios', [
            'Ropa Tradicional',
            'Vestidos Típicos',
            'Accesorios de Moda',
            'Zapatos y Sandalias',
            'Bolsos y Carteras'
        ]),
        ('Hogar y Decoración', [
            'Muebles Típicos',
            'Decoración con Madera',
            'Textiles para Hogar',
            'Arte Wall Art',
            'Productos de Bambú'
        ]),
        ('Tecnología y Electrónicos', [
            'Dispositivos Electrónicos',
            'Accesorios para Celulares',
            'Equipos de Computación',
            'Reparación de Equipos',
            'Servicios Técnicos'
        ]),
        ('Servicios', [
            'Clases de Cocina Típica',
            'Talleres Artesanales',
            'Transporte',
            'Eventos Culturales'
        ])
    ]

    for name, subcategories in categories_data:
        parent = Category.objects.create(name=name)
        for subcat in subcategories:
            Category.objects.create(name=subcat, parent=parent)

class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0002_initial'),  # Replace with your last migration
    ]

    operations = [
        migrations.RunPython(create_categories),
    ]