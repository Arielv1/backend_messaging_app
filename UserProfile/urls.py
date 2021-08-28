from .views import RegisterAPI, LoginAPI
from django.urls import path
from knox import views as knox_views
from . import views
urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    # path('register/', views.register, name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('deleteall/', views.delete_all_users, name="deleteall")
]
