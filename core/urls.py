from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sobre/', views.sobre, name='sobre'),
    path('contato/', views.contato, name='contato'),
    path('produtos/', views.produtos, name='produtos'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('painel/', views.admin_produtos, name='admin_produtos'),
    path('painel/novo/', views.produto_criar, name='produto_criar'),
    path('painel/editar/<int:pk>/', views.produto_editar, name='produto_editar'),
    path('painel/excluir/<int:pk>/', views.produto_excluir, name='produto_excluir'),
]