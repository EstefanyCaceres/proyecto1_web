from django import forms
from .models import Libro,Prestamo

class PrestamoForm(forms.ModelForm):
    class Meta:
        model = Prestamo  
        fields = [ 'titulo_libro', 'fecha_devolucion', 'devuelto']  
        labels = {
            'titulo_libro': 'Libro',
            'fecha_devolucion': 'Fecha Devolucion',
            
        }
        widgets = {
            'titulo_libro': forms.Select(attrs={'id': 'titulo_libro'}),
            'fecha_devolucion': forms.DateInput(attrs={'id': 'fecha_devolucion','type':'date'}),
           
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['titulo_libro'].queryset = Libro.objects.filter(disponible=True)
        self.fields['titulo_libro'].empty_label = 'Seleccione un libro'

class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro  
        fields = ['titulo', 'autor', 'editorial', 'disponible']  
        labels = {
            'titulo': 'Título',
            'autor': 'Autor',
            'editorial': 'Editorial',
            
        }
        widgets = {
            'titulo': forms.TextInput(attrs={'id': 'titulo'}),
            'autor': forms.TextInput(attrs={'id': 'autor'}),
            'editorial': forms.TextInput(attrs={'id': 'editorial'}),
            
        }
