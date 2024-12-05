from django.urls import path

from . import views

urlpatterns = [
    path("", views.editor, name="editor"),
    path("auth-callback", views.callback, name="auth-callback"),
    path("login", views.login, name="login")
]