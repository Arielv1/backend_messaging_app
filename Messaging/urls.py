from django.contrib import admin
from django.urls import include, path
from . import views
# Create your views here.

urlpatterns = [
    path('send/', views.send, name="send"),
    path('read/', views.read, name="read"),
    path('delete/', views.delete, name="delete"),
    path('deleteall', views.delete_all_messages, name="deleteall"),
    path('showall/', views.show_all_messages, name="showall"),
    path('showallunread/',
         views.show_all_unread_messages, name="showallunread")
]
