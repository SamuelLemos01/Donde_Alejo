
# Create your models here.


from django.db import models # type: ignore

class Product(models.Model):
    imagen = models.ImageField(upload_to='menu_images/')
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    
    
    def __str__(self):
        return self.nombre



