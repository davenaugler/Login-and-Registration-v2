from django.urls import path
from . import views

urlpatterns = [
    path('', views.Login_Reg),
    path('register', views.Register),
    path('login', views.Login),
    path('success', views.Success),
    path('logout', views.Logout)
]