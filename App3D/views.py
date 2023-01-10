from django.shortcuts import render
from .models import Blog, Avatar
from django.http import HttpResponse


from django.urls import reverse_lazy

from App3D.forms import  RegistroUsuarioForm, UserEditForm, AvatarForm,  MessageForm

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, authenticate

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required 




from django.shortcuts import render
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from .models import CanalMensaje, CanalUsuario, Canal
from django.http import HttpResponse, Http404, JsonResponse

from .forms import FormMensajes

from django.views.generic.edit import FormMixin

from django.views.generic import View
# Create your views here.
from django.shortcuts import render


def obtenerAvatar(request):
    lista=Avatar.objects.filter(user=request.user)
    if len(lista)!=0:
        imagen=lista[0].imagen.url
    else:
        imagen="/media/avatares/avatarpordefecto.jpg"
    return imagen

@login_required
def inicio(request):
    lista=Avatar.objects.filter(user=request.user)
    
    return render (request, "App3D/inicio.html", {"imagen":obtenerAvatar(request)})




    return render (request, "App3D/inicio.html")





def leerBlogs(request):
    listaBlogs=Blog.objects.all()
    print(listaBlogs)
    return render(request, "App3D/leerBlogs.html", {"listaBlogs":listaBlogs})


@login_required   
def detalleBlog(request, id):
    blog=Blog.objects.get(id=id)

    return render(request, "App3D/detalleBlog.html",{"blog":blog})






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

            return render(request, "App3D/RegistrOk.html", {"mensaje":f"Usuario {username} creado correctamente"})
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
            usuario.web=info["web"]
            usuario.descripcion=info["descripcion"]

            usuario.save()
            return render(request, "App3D/inicio.html", {"mensaje":"Perfil editado correctamente"})
        else:
            return render(request, "App3D/editarUsuario.html", {"form":form, "nombreusuario":usuario.username, "mensaje":"Error al editar el perfil"})
    else:
        form=UserEditForm(instance=usuario)
        return render(request, "App3D/editarPerfil.html", {"form":form, "nombreusuario":usuario.username})

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



class Inbox(View):
	def get(self, request):

		inbox = Canal.objects.filter(canalusuario__usuario__in=[request.user.id])


		context = {

			"inbox":inbox
		}

		return render(request, 'App3D/inbox.html', context)


class CanalFormMixin(FormMixin):
	form_class =FormMensajes


	def get_success_url(self):
		return self.request.path

	def post(self, request, *args, **kwargs):

		if not request.user.is_authenticated:
			raise PermissionDenied

		form = self.get_form()
		if form.is_valid():
			canal = self.get_object()
			usuario = self.request.user 
			mensaje = form.cleaned_data.get("mensaje")
			canal_obj = CanalMensaje.objects.create(canal=canal, usuario=usuario, texto=mensaje)
			
			if request.is_ajax():
				return JsonResponse({

					'mensaje':canal_obj.texto,
					'username':canal_obj.usuario.username
					}, status=201)

			return super().form_valid(form)

		else:

			if request.is_ajax():
				return JsonResponse({"Error":form.errors}, status=400)

			return super().form_invalid(form)

class CanalDetailView(LoginRequiredMixin, CanalFormMixin, DetailView):
	template_name= 'App3D/Dm/canal_detail.html'
	queryset = Canal.objects.all()

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)

		obj = context['object']
		print(obj)



		context['si_canal_mienbro'] = self.request.user in obj.usuarios.all()

		return context



class DetailMs(LoginRequiredMixin, CanalFormMixin, DetailView):

	template_name= 'App3D/Dm/canal_detail.html'

	def get_object(self, *args, **kwargs):

		username = self.kwargs.get("username")
		mi_username = self.request.user.username
		canal, _ = Canal.objects.obtener_o_crear_canal_ms(mi_username, username)

		if username == mi_username:
			mi_canal, _ = Canal.objects.obtener_o_crear_canal_usuario_actual(self.request.user)

			return mi_canal

		if canal == None:
			raise Http404

		return canal

def mensajes_privados(request, username, *args, **kwargs):

	if not request.user.is_authenticated:
		return HttpResponse("Prohibido")

	mi_username = request.user.username

	canal, created = Canal.objects.obtener_o_crear_canal_ms(mi_username, username)

	if created:
		print("Si, fue creado")

	Usuarios_Canal = canal.canalusuario_set.all().values("usuario__username")
	print(Usuarios_Canal)
	mensaje_canal  = canal.canalmensaje_set.all()
	print(mensaje_canal.values("texto"))

	return HttpResponse(f"Nuestro Id del Canal - {canal.id}")