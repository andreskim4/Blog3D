
from django.urls import path, re_path
from App3D.views import *
from django.contrib.auth.views import LogoutView
UUID_CANAL_REGEX = r'canal/(?P<pk>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})'

urlpatterns = [
    path('', inicio, name="inicio"),
    path("pages/", leerBlogs, name="leerBlogs"),
    path("pages/<id>", detalleBlog, name="detalleBlog"),



    path('login/', login_request, name='login'),
    path('account/signup', register, name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("editarPerfil/", editarPerfil, name='editarPerfil'),
    path("agregarAvatar/", agregarAvatar, name="agregarAvatar"),


    re_path(UUID_CANAL_REGEX, CanalDetailView.as_view()),
	path("dm/<str:username>", mensajes_privados),
	path("ms/<str:username>", DetailMs.as_view(), name="detailms"),
    path("inbox/", Inbox.as_view(), name="inbox"),

]