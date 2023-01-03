
from django.urls import path
from App3D.views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [

    path("usuario/", usuario, name="usuario"),
    path("", inicio, name="inicio"),
    path("leerUsuario/", leerUsuario, name="leerUsuario"),
    path("eliminarusuario/<id>", eliminarUsuario, name="eliminarusuario"),
    path("editarusuario/<id>", editarUsuario, name="editarusuario"),


    path('login/', login_request, name='login'),
    path('register/', register, name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("editarPerfil/", editarPerfil, name='editarPerfil'),
    path("agregarAvatar/", agregarAvatar, name="agregarAvatar"),

]