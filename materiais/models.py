from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Categoria(models.Model):
    TIPOS_CATEGORIA = [
        ('escritorio', 'Escritório'),
        ('limpeza', 'Limpeza'),
        ('manutencao', 'Manutenção'),
    ]
    
    nome = models.CharField(max_length=100, unique=True)
    tipo = models.CharField(max_length=20, choices=TIPOS_CATEGORIA)
    descricao = models.TextField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['tipo', 'nome']
    
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.nome}"



class Material(models.Model):
    nome = models.CharField(max_length=200)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='materiais')
    descricao = models.TextField(blank=True, null=True)
    unidade_medida = models.CharField(max_length=20, default='unidade')
    quantidade_atual = models.PositiveIntegerField(default=0)
    reservado = models.PositiveIntegerField(default=0)  # 🔥 Novo campo
    quantidade_minima = models.PositiveIntegerField(default=5)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    fornecedor = models.CharField(max_length=200, blank=True, null=True)
    localizacao = models.CharField(max_length=100, blank=True, null=True)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Material'
        verbose_name_plural = 'Materiais'
        ordering = ['categoria', 'nome']
    
    def __str__(self):
        return f"{self.nome} ({self.categoria.tipo})"
    
    @property
    def estoque_baixo(self):
        return self.quantidade_atual <= self.quantidade_minima
    
    @property
    def valor_total_estoque(self):
        if self.preco_unitario:
            return self.quantidade_atual * self.preco_unitario
        return 0


class MovimentacaoEstoque(models.Model):
    """Modelo para registrar movimentações de entrada e saída do estoque"""
    TIPOS_MOVIMENTACAO = [
        ('entrada', 'Entrada'),
        ('saida', 'Saída'),
        ('ajuste', 'Ajuste'),
    ]
    
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='movimentacoes')
    tipo = models.CharField(max_length=10, choices=TIPOS_MOVIMENTACAO)
    quantidade = models.IntegerField()
    quantidade_anterior = models.PositiveIntegerField()
    quantidade_nova = models.PositiveIntegerField()
    motivo = models.CharField(max_length=200)
    observacoes = models.TextField(blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    data_movimentacao = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = 'Movimentação de Estoque'
        verbose_name_plural = 'Movimentações de Estoque'
        ordering = ['-data_movimentacao']
    
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.material.nome} - {self.quantidade}"


class Fornecedor(models.Model):
    """Modelo para fornecedores"""
    nome = models.CharField(max_length=200)
    cnpj = models.CharField(max_length=18, blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    endereco = models.TextField(blank=True, null=True)
    contato_responsavel = models.CharField(max_length=100, blank=True, null=True)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Fornecedor'
        verbose_name_plural = 'Fornecedores'
        ordering = ['nome']
    
    def __str__(self):
        return self.nome


class SolicitacaoCompra(models.Model):
    """Modelo para solicitações de compra"""
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('aprovada', 'Aprovada'),
        ('rejeitada', 'Rejeitada'),
        ('comprada', 'Comprada'),
    ]
    
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantidade_solicitada = models.PositiveIntegerField()
    justificativa = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    solicitante = models.ForeignKey(User, on_delete=models.CASCADE, related_name='solicitacoes')
    aprovador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='aprovacoes', null=True, blank=True)
    data_solicitacao = models.DateTimeField(auto_now_add=True)
    data_aprovacao = models.DateTimeField(null=True, blank=True)
    observacoes_aprovador = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Solicitação de Compra'
        verbose_name_plural = 'Solicitações de Compra'
        ordering = ['-data_solicitacao']
    
    def __str__(self):
        return f"Solicitação {self.id} - {self.material.nome}"

