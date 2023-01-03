from django.shortcuts import render
from .models import usuario, Avatar
from django.http import HttpResponse


from django.urls import reverse_lazy

from App3D.forms import UsuarioForm, RegistroUsuarioForm, UserEditForm, AvatarForm,  MessageForm

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, authenticate

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required  

# Create your views here.
from django.shortcuts import render



def obtenerAvatar(request):
    lista=Avatar.objects.filter(user=request.user)
    if len(lista)!=0:
        imagen=lista[0].imagen.url
    else:
        imagen="/media/avatares/avatarpordefecto.png"
    return imagen

@login_required
def inicio(request):
    lista=Avatar.objects.filter(user=request.user)
    
    return render (request, "App3D/inicio.html", {"imagen":obtenerAvatar(request)})


    

    return render (request, "App3D/inicio.html")


@login_required
def usuario(request):

    if request.method=="POST":
        form=usuarioForm(request.POST)
        if form.is_valid():
            informacion=form.cleaned_data
            print(informacion)
            nombre=informacion["nombre"]
            apellido=informacion["apellido"]
            email=informacion["email"]
            profesion=informacion["profesion"]
            usuario= usuario(nombre=nombre, apellido=apellido, email=email, profesion=profesion)
            usuario.save()
            return render (request, "App3D/inicio.html", {"mensaje": "SEÑOR USUARIO CREADO CORRECTAMENTE!!", "imagen":obtenerAvatar(request)})
    else:
        formulario=usuarioForm()


    return render (request, "App3D/usuario.html", {"form":formulario, "imagen":obtenerAvatar(request)})





def leerUsuario(request):
    usuario=usuario.objects.all()
    print(usuario)
    return render(request, "App3D/leerUsuario.html", {"usuario":usuario})

@login_required
def eliminarUsuario(request, id):
    usuario=usuario.objects.get(id=id)
    usuario.delete()
    usuario=usuario.objects.all()
    return render(request, "App3D/leerUsuario.html", {"mensaje":"Usuario eliminado correctamente", "usuario":usuario})

@login_required   
def editarUsuario(request, id):
    usuario=usuario.objects.get(id=id)
    if request.method=="POST":
        form=usuarioForm(request.POST)
        print(form)
        if form.is_valid():
            informacion=form.cleaned_data
            print(informacion)
                  
            
            usuario.nombre=informacion["nombre"]
            usuario.apellido=informacion["apellido"]
            usuario.email=informacion["email"]
            usuario.profesion=informacion["profesion"]
            usuario.save()
            usuario=usuario.objects.all()
            return render (request, "App3D/leerUsuario.html", {"mensaje": "USUARIO EDITADO CORRECTAMENTE!!", "usuario":usuario})
    else:
        formulario= usuarioForm(initial={"nombre":usuario.nombre, "apellido":usuario.apellido, "email":usuario.email, "profesion":usuario.profesion})
    return render(request, "App3D/editarUsuario.html", {"form":formulario, "usuario":usuario})




#Vistas basadas en clases





#----- seccion de login ------

def login_request(request):
    if request.method == "POST":
        form=AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            usu=form.cleaned_data.get("username")
            clave=form.cleaned_data.get("password")

            usuario=authenticate(username=usu, password=clave)#trae un usuario de la base, que tenga ese usuario y ese pass, si existe, lo trae y si no None
            if usuario is not None:    
                login(request, usuario)
                return render(request, 'App3D/inicio.html', {'mensaje':f"Bienvenido {usuario}" })
            else:
                return render(request, 'App3D/login.html', {'mensaje':"Usuario o contraseña incorrectos", 'form':form})

        else:
            return render(request, 'App3D/login.html', {'mensaje':"Usuario o contraseña incorrectos", 'form':form})

    else:
        form = AuthenticationForm()
    return render(request, "App3D/login.html", {"form":form})



def register(request):
    if request.method=="POST":
        form=RegistroUsuarioForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get("username")
            form.save()
            #aca se podria loguear el usuario, con authenticate y login... pero no lo hago
            return render(request, "App3D/inicio.html", {"mensaje":f"Usuario {username} creado correctamente"})
        else:
            return render(request, "App3D/register.html", {"form":form, "mensaje":"Error al crear el usuario"})
        
    else:
        form=RegistroUsuarioForm()
    return render(request, "App3D/register.html", {"form":form})

@login_required
def editarPerfil(request):
    usuario=request.user
    if request.method=="POST":
        form=UserEditForm(request.POST)
        if form.is_valid():
            info=form.cleaned_data
            usuario.email=info["email"]
            usuario.password1=info["password1"]
            usuario.password2=info["password2"]
            usuario.first_name=info["first_name"]
            usuario.last_name=info["last_name"]
            usuario.save()
            return render(request, "App3D/inicio.html", {"mensaje":"Perfil editado correctamente"})
        else:
            return render(request, "App3D/editarUsuario.html", {"form":form, "nombreusuario":usuario.username, "mensaje":"Error al editar el perfil"})
    else:
        form=UserEditForm(instance=usuario)
        return render(request, "App3D/editarUsuario.html", {"form":form, "nombreusuario":usuario.username})

@login_required
def agregarAvatar(request):
    if request.method=="POST":
        form=AvatarForm(request.POST, request.FILES)#ademas del post, como trae archivos (yo se que trae archivos xq conozco el form, tengo q usar request.files)
        if form.is_valid():
            avatarViejo=Avatar.objects.filter(user=request.user)
            if len(avatarViejo)!=0:
                avatarViejo[0].delete()
            avatar=Avatar(user=request.user, imagen=request.FILES["imagen"])
            avatar.save()
            return render(request, "App3D/inicio.html", {"mensaje":"Avatar agregado correctamente"})
        else:
            return render(request, "App3D/AgregarAvatar.html", {"formulario": form, "usuario": request.user})
    else:
        form=AvatarForm()
        return render(request , "App3D/AgregarAvatar.html", {"formulario": form, "usuario": request.user})
   
def chat_view(request):
    return render(request, 'chat.html')
 
def chat_view(request):
    form = MessageForm()
    messages = Message.objects.all()
    return render(request, 'chat.html', {'form': form, 'messages': messages})
