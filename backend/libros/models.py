from django.db import models
from accounts.models import *

class LibroUser(models.Model):
    isbn = models.CharField(max_length=15, null=False, unique=True, primary_key=True)
    titulo = models.CharField(max_length=20, null=False)
    librosComprados = models.IntegerField(null=False,default=0)
    user = models.ForeignKey(User,on_delete= models.CASCADE)
    class Meta:
        verbose_name_plural = "Libro"
        
class LibroAdmin(models.Model):
    """
    Model representing a book.
    """
    isbn = models.CharField(max_length=15, null=False, unique=True, primary_key=True)
    titulo = models.CharField(max_length=20, null=False)
    precioCompra = models.IntegerField(null=False)
    precioVenta = models.IntegerField(null=False)
    stock = models.IntegerField(null=False)
    class Meta:
        verbose_name_plural = "LibroAdmin"

class Transacion(models.Model):
    """
    Model representing a transaction.
    """
    id = models.AutoField(primary_key=True)
    tipo_transaccion = models.CharField(max_length=15,null=False)
    fecha_realizacion = models.DateTimeField(auto_now_add=True)
    cantidad_ejemplares = models.IntegerField(null=False)
    libro = models.ForeignKey(LibroAdmin, on_delete=models.CASCADE)# se hara one to many poque un libro puede tener muchas transacciones
    class Meta:
        verbose_name_plural = "Transaccion"
    

