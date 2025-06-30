from django import forms
from .models import Material, Categoria, MovimentacaoEstoque, SolicitacaoCompra


class MaterialForm(forms.ModelForm):
    """Formulário para criação e edição de materiais"""
    
    class Meta:
        model = Material
        fields = [
            'nome', 'categoria', 'descricao', 'unidade_medida',
            'quantidade_atual', 'quantidade_minima', 'preco_unitario',
            'fornecedor', 'localizacao'
        ]
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do material'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descrição do material'}),
            'unidade_medida': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: unidade, kg, litro'}),
            'quantidade_atual': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'quantidade_minima': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'preco_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'fornecedor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do fornecedor'}),
            'localizacao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Local de armazenamento'}),
        }
        labels = {
            'nome': 'Nome do Material',
            'categoria': 'Categoria',
            'descricao': 'Descrição',
            'unidade_medida': 'Unidade de Medida',
            'quantidade_atual': 'Quantidade Atual',
            'quantidade_minima': 'Quantidade Mínima',
            'preco_unitario': 'Preço Unitário (R$)',
            'fornecedor': 'Fornecedor',
            'localizacao': 'Localização',
        }


class MovimentacaoForm(forms.ModelForm):
    """Formulário para movimentação de estoque"""
    
    class Meta:
        model = MovimentacaoEstoque
        fields = ['tipo', 'quantidade', 'motivo', 'observacoes']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'motivo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Motivo da movimentação'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Observações adicionais'}),
        }
        labels = {
            'tipo': 'Tipo de Movimentação',
            'quantidade': 'Quantidade',
            'motivo': 'Motivo',
            'observacoes': 'Observações',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customiza o campo quantidade baseado no tipo
        self.fields['quantidade'].help_text = 'Para ajuste, informe a quantidade final desejada'


class SolicitacaoCompraForm(forms.ModelForm):
    """Formulário para solicitação de compra"""
    
    class Meta:
        model = SolicitacaoCompra
        fields = ['material', 'quantidade_solicitada', 'justificativa']
        widgets = {
            'material': forms.Select(attrs={'class': 'form-control'}),
            'quantidade_solicitada': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'justificativa': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Justifique a necessidade da compra'}),
        }
        labels = {
            'material': 'Material',
            'quantidade_solicitada': 'Quantidade Solicitada',
            'justificativa': 'Justificativa',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtra apenas materiais ativos
        self.fields['material'].queryset = Material.objects.filter(ativo=True).order_by('categoria', 'nome')


class CategoriaForm(forms.ModelForm):
    """Formulário para criação e edição de categorias"""
    
    class Meta:
        model = Categoria
        fields = ['nome', 'tipo', 'descricao']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da categoria'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descrição da categoria'}),
        }
        labels = {
            'nome': 'Nome da Categoria',
            'tipo': 'Tipo',
            'descricao': 'Descrição',
        }


class FiltroMaterialForm(forms.Form):
    """Formulário para filtros na listagem de materiais"""
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),
        required=False,
        empty_label="Todas as categorias",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    busca = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Buscar por nome, descrição ou fornecedor'})
    )
    estoque_baixo = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria'].label = 'Categoria'
        self.fields['busca'].label = 'Buscar'
        self.fields['estoque_baixo'].label = 'Apenas estoque baixo'

