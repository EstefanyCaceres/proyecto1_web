from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Libro,Prestamo
from django.db import transaction
from .forms import PrestamoForm,LibroForm
from django.db.models import Q #importar Q para busquedas query
from django.contrib import messages #mensajes para usar como flask

# Create your views here.

def index(request):
    libros = Libro.objects.all()
    titulos = libros.values_list('titulo', flat=True).distinct()
    autores = libros.values_list('autor', flat=True).distinct()
    return render(request, 'libros/index.html', {
        'titulos': list(titulos),
        'autores': list(autores)
    })

def resultados(request):
    busqueda = request.GET.get('nombrelibro').strip() # Obtener el término de búsqueda y eliminar espacios en blanco con strip
    libros = Libro.objects.filter(
        Q(titulo__icontains=busqueda) | 
        Q(autor__icontains=busqueda) |
        Q(titulo__iexact=busqueda) |
        Q(autor__iexact=busqueda)
    ).order_by('titulo')
    if(not libros.exists()):
        messages.info(request, 'No se encontraron resultados para tu búsqueda.') #se envia el mensaje
        return redirect('index')
    else:
        return render(request, 'libros/resultados.html', {'busqueda': busqueda, 'libros': libros})

def login_view(request):
    if request.method == "POST":
        user = authenticate(request, username=request.POST.get("username"),password=request.POST.get("password"))

        if user:
            login(request,user)
            return redirect('menu')
        
        messages.info(request, 'Usuario o Contraseña inválidos.') #se envia el mensaje
        return redirect('libros/login.html')
    return render(request, 'libros/login.html')


@login_required
def menu(request):
    return render(request, 'libros/menu.html')

@login_required
def libros(request):
    libros = Libro.objects.all().order_by('titulo')
    return render(request, 'libros/consultar_libros.html',{'libros':libros})

@login_required
def prestamos(request):
    prestamos = Prestamo.objects.order_by('devuelto', '-fecha_prestamo')

    if not (request.user.is_staff or request.user.is_superuser):
        prestamos=prestamos.filter(nombre_usuario=request.user)
    return render(request, 'libros/consultar_prestamos.html',{'prestamos':prestamos})


@login_required
def realizar_prestamo(request, libro_id):
    libro = Libro.objects.get(id=libro_id)
    if request.method=='POST':
        form = PrestamoForm(request.POST)
        if form.is_valid():
            prestamo= form.save(commit=False)
            prestamo.nombre_usuario=request.user
            prestamo.save()
            
            libro = prestamo.titulo_libro
            if libro and not prestamo.devuelto and libro.disponible:
                libro.disponible = False
                libro.save(update_fields=['disponible'])
            if(not request.user.is_staff or not request.user.is_superuser):
                return redirect('libros')
            
    
    else:
        # Inicializar el formulario con el libro seleccionado para que aparezca pre-seleccionado
        form = PrestamoForm(initial={'titulo_libro': libro})
        # Asegurar que el queryset del campo incluya el libro seleccionado incluso si su disponibilidad cambió
        try:
            # unir querysets para incluir tanto libros disponibles como el libro específico
            form.fields['titulo_libro'].queryset = (
                Libro.objects.filter(disponible=True) | Libro.objects.filter(pk=libro.pk)
            )
        except Exception:
            # en caso de cualquier problema, dejar el queryset por defecto
            pass
    return render(request, 'libros/realizar_prestamo.html',{'form':form, 'libro':libro})


@login_required
def agregar_libro(request):
    if request.method=='POST':
        form = LibroForm(request.POST)
        if form.is_valid():
            libro= form.save(commit=False)
            libro.save()
            
            return redirect('libros')
    
    else:
        form = LibroForm()
    return render(request, 'libros/agregar_libro.html',{'form':form})

@login_required
def eliminar_libro(request, libro_id):
    libro = Libro.objects.get(id=libro_id)
    if request.method == 'POST':
        libro.delete()
        return redirect('libros')
    return render(request, 'libros/eliminar_libro.html', {'libro': libro})

@login_required
def editar_libro(request, libro_id):
    libro = Libro.objects.get(id=libro_id)
    if request.method == 'POST':
        form = LibroForm(request.POST, instance=libro)
        if form.is_valid():
            form.save()
            return redirect('libros')
    else:
        form = LibroForm(instance=libro)
    return render(request, 'libros/editar_libro.html', {'form': form})


@login_required
def devolver_prestamo(request, prestamo_id):
    # Solo el admin (o superuser) puede marcar devoluciones
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('prestamos')

    prestamo = get_object_or_404(Prestamo, id=prestamo_id)

    if request.method == 'POST':
        with transaction.atomic():
            prestamo.devuelto = True
            prestamo.save(update_fields=['devuelto'])

            if prestamo.titulo_libro:
                libro = prestamo.titulo_libro
                libro.disponible = True
                libro.save(update_fields=['disponible'])

        return redirect('prestamos')

    return redirect('prestamos')

def logout_view(request):
    logout(request)              
    return redirect('index')     