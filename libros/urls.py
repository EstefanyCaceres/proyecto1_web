from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('resultados/', views.resultados, name='resultados'),
    path('menu/', views.menu, name='menu'),
    path('logout/', views.logout_view, name='logout'),
    path('libros/', views.libros, name='libros'),
    path('prestamos/', views.prestamos, name='prestamos'),
    path('realizar-prestamo/<int:libro_id>/', views.realizar_prestamo, name='realizar_prestamo'),
    path('prestamos/<int:prestamo_id>/devolver/', views.devolver_prestamo, name='devolver_prestamo'),
    path('agregar-libro/', views.agregar_libro, name='agregar_libro'),
    path('libros/eliminar/<int:libro_id>/', views.eliminar_libro, name='eliminar_libro'),
    path('libros/editar/<int:libro_id>/', views.editar_libro, name='editar_libro'),
]