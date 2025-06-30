from django.urls import path
from . import views

urlpatterns = [
    # Autenticação
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Materiais
    path('materiais/', views.lista_materiais, name='lista_materiais'),
    path('materiais/adicionar/', views.adicionar_material, name='adicionar_material'),
    path('materiais/<int:material_id>/', views.detalhe_material, name='detalhe_material'),
    path('materiais/<int:material_id>/editar/', views.editar_material, name='editar_material'),
    path('materiais/<int:material_id>/movimentar/', views.movimentar_estoque, name='movimentar_estoque'),
    
    # Relatórios
    path('relatorio/', views.relatorio_estoque, name='relatorio_estoque'),
    
    # Solicitações de compra
    path('solicitacoes/', views.solicitacoes_compra, name='solicitacoes_compra'),
    path('solicitacoes/nova/', views.nova_solicitacao_compra, name='nova_solicitacao_compra'),
    path('solicitacoes/<int:solicitacao_id>/aprovar/', views.aprovar_solicitacao, name='aprovar_solicitacao'),
]

