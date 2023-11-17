
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('support/', views.support, name='support'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('faq/', views.faq, name='faq'),
    path('policy/', views.policy, name='policy'),
]
