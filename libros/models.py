from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=200)
    editorial = models.CharField(max_length=200)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.titulo

class Prestamo(models.Model):
    nombre_usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo_libro = models.ForeignKey(Libro, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_prestamo = models.DateField(auto_now_add=True)
    fecha_devolucion = models.DateField(null=True, blank=True)
    devuelto=models.BooleanField(default=False)

    def __str__(self):
        libro = self.titulo_libro.titulo if self.titulo_libro else "Prestamo"
        return f"{libro} → {self.nombre_usuario.username}"
