from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.home, name='home' ),
    path('about', views.about, name='about' ),
    path('services', views.services, name='services' ),
    path('contact', views.contact, name='contact' ),
    path('scann', views.scann, name='scann'),
    path('lan_scann', views.lan_scann, name='lan-scann'),
    path('pass_scann', views.pass_scann, name='pass_scann'),
    path('domain_enum', views.domain_enum, name='domain_enum'),
    path('google_dork', views.google_dork, name='google_dork'),
    path('Evo_os', views.Evo_os, name='Evo_os'),
    path('login', views.login, name='login'),
]