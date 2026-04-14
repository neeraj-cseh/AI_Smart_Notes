from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_note, name='create_note'),
    path('summarize/<int:note_id>/', views.summarize_note, name='summarize_note'),
]