from django.contrib import admin
from dondealejo.models import Product

# Aquí solo registramos una vez
class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ('imagen', 'nombre', 'descripcion', 'precio')
admin.site.register(Product, ProductAdmin)  # Solo este registro
