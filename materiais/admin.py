from django.contrib import admin
from .models import Categoria, Material, MovimentacaoEstoque, Fornecedor, SolicitacaoCompra


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'tipo', 'criado_em']
    list_filter = ['tipo', 'criado_em']
    search_fields = ['nome', 'descricao']
    ordering = ['tipo', 'nome']


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['nome', 'categoria', 'quantidade_atual', 'quantidade_minima', 'estoque_baixo', 'ativo']
    list_filter = ['categoria__tipo', 'categoria', 'ativo', 'criado_em']
    search_fields = ['nome', 'descricao', 'fornecedor']
    ordering = ['categoria', 'nome']
    list_editable = ['quantidade_atual', 'quantidade_minima', 'ativo']
    
    def estoque_baixo(self, obj):
        return obj.estoque_baixo
    estoque_baixo.boolean = True
    estoque_baixo.short_description = 'Estoque Baixo'


@admin.register(MovimentacaoEstoque)
class MovimentacaoEstoqueAdmin(admin.ModelAdmin):
    list_display = ['material', 'tipo', 'quantidade', 'quantidade_anterior', 'quantidade_nova', 'usuario', 'data_movimentacao']
    list_filter = ['tipo', 'data_movimentacao', 'material__categoria']
    search_fields = ['material__nome', 'motivo', 'observacoes']
    ordering = ['-data_movimentacao']
    readonly_fields = ['data_movimentacao']


@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cnpj', 'telefone', 'email', 'ativo']
    list_filter = ['ativo', 'criado_em']
    search_fields = ['nome', 'cnpj', 'email', 'contato_responsavel']
    ordering = ['nome']
    list_editable = ['ativo']


@admin.register(SolicitacaoCompra)
class SolicitacaoCompraAdmin(admin.ModelAdmin):
    list_display = ['id', 'material', 'quantidade_solicitada', 'status', 'solicitante', 'data_solicitacao']
    list_filter = ['status', 'data_solicitacao', 'material__categoria']
    search_fields = ['material__nome', 'justificativa', 'solicitante__username']
    ordering = ['-data_solicitacao']
    readonly_fields = ['data_solicitacao']

