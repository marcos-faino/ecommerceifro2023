from django.urls import path
from . import views

urlpatterns = [
    path('cadusuario/', views.CadUsuarioView.as_view(), name='cadusuario'),
    path('cadmeuusuario/<int:id>', views.CadMeuUsuarioView.as_view(), name='cadmeuusuario'),
    path('login/', views.LoginUsuarioView.as_view(), name='loginuser'),
    path('logout/', views.LogoutView.as_view(), name='logoutuser'),
]