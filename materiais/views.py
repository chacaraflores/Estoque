from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q, Sum, F
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import Material, Categoria, MovimentacaoEstoque, Fornecedor, SolicitacaoCompra
from .forms import MaterialForm, MovimentacaoForm, SolicitacaoCompraForm
import json


def login_view(request):
    """View para login do usuário"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    return render(request, 'materiais/login.html')


def logout_view(request):
    """View para logout do usuário"""
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    """Dashboard principal do sistema"""
    # Estatísticas gerais
    total_materiais = Material.objects.filter(ativo=True).count()
    materiais_estoque_baixo = Material.objects.filter(ativo=True, quantidade_atual__lte=F('quantidade_minima')).count()
    
    # Materiais com estoque baixo
    materiais_baixo = Material.objects.filter(
        ativo=True, 
        quantidade_atual__lte=F('quantidade_minima')
    ).order_by('quantidade_atual')[:10]
    
    # Últimas movimentações
    ultimas_movimentacoes = MovimentacaoEstoque.objects.select_related('material', 'usuario').order_by('-data_movimentacao')[:10]
    
    # Solicitações pendentes
    solicitacoes_pendentes = SolicitacaoCompra.objects.filter(status='pendente').count()
    
    # Estatísticas por categoria
    from django.db.models import Count
    stats_categoria = Categoria.objects.annotate(
        total_materiais=Count('materiais', filter=Q(materiais__ativo=True)),
        valor_total=Sum(
            F('materiais__quantidade_atual') * F('materiais__preco_unitario'),
            filter=Q(materiais__ativo=True)
        )
    )
    
    context = {
        'total_materiais': total_materiais,
        'materiais_estoque_baixo': materiais_estoque_baixo,
        'materiais_baixo': materiais_baixo,
        'ultimas_movimentacoes': ultimas_movimentacoes,
        'solicitacoes_pendentes': solicitacoes_pendentes,
        'stats_categoria': stats_categoria,
    }
    return render(request, 'materiais/dashboard.html', context)


@login_required
def lista_materiais(request):
    """Lista todos os materiais com filtros"""
    materiais = Material.objects.filter(ativo=True).select_related('categoria')
    
    # Filtros
    categoria_id = request.GET.get('categoria')
    busca = request.GET.get('busca')
    estoque_baixo = request.GET.get('estoque_baixo')
    
    if categoria_id:
        materiais = materiais.filter(categoria_id=categoria_id)
    
    if busca:
        materiais = materiais.filter(
            Q(nome__icontains=busca) | 
            Q(descricao__icontains=busca) |
            Q(fornecedor__icontains=busca)
        )
    
    if estoque_baixo:
        materiais = materiais.filter(quantidade_atual__lte=F('quantidade_minima'))
    
    categorias = Categoria.objects.all()
    
    context = {
        'materiais': materiais,
        'categorias': categorias,
        'categoria_selecionada': categoria_id,
        'busca': busca,
        'estoque_baixo': estoque_baixo,
    }
    return render(request, 'materiais/lista_materiais.html', context)


@login_required
def detalhe_material(request, material_id):
    """Exibe detalhes de um material específico"""
    material = get_object_or_404(Material, id=material_id, ativo=True)
    movimentacoes = material.movimentacoes.order_by('-data_movimentacao')[:20]
    
    context = {
        'material': material,
        'movimentacoes': movimentacoes,
    }
    return render(request, 'materiais/detalhe_material.html', context)


@login_required
def adicionar_material(request):
    """Adiciona um novo material"""
    if request.method == 'POST':
        form = MaterialForm(request.POST)
        if form.is_valid():
            material = form.save()
            messages.success(request, f'Material "{material.nome}" adicionado com sucesso!')
            return redirect('lista_materiais')
    else:
        form = MaterialForm()
    
    return render(request, 'materiais/form_material.html', {'form': form, 'titulo': 'Adicionar Material'})


@login_required
def editar_material(request, material_id):
    """Edita um material existente"""
    material = get_object_or_404(Material, id=material_id, ativo=True)
    
    if request.method == 'POST':
        form = MaterialForm(request.POST, instance=material)
        if form.is_valid():
            form.save()
            messages.success(request, f'Material "{material.nome}" atualizado com sucesso!')
            return redirect('detalhe_material', material_id=material.id)
    else:
        form = MaterialForm(instance=material)
    
    return render(request, 'materiais/form_material.html', {
        'form': form, 
        'titulo': 'Editar Material',
        'material': material
    })


@login_required
def movimentar_estoque(request, material_id):
    """Registra movimentação de estoque"""
    material = get_object_or_404(Material, id=material_id, ativo=True)
    
    if request.method == 'POST':
        form = MovimentacaoForm(request.POST)
        if form.is_valid():
            movimentacao = form.save(commit=False)
            movimentacao.material = material
            movimentacao.usuario = request.user
            movimentacao.quantidade_anterior = material.quantidade_atual
            
            # Calcula nova quantidade
            if movimentacao.tipo == 'entrada':
                nova_quantidade = material.quantidade_atual + movimentacao.quantidade
            elif movimentacao.tipo == 'saida':
                nova_quantidade = max(0, material.quantidade_atual - movimentacao.quantidade)
            else:  # ajuste
                nova_quantidade = movimentacao.quantidade
            
            movimentacao.quantidade_nova = nova_quantidade
            movimentacao.save()
            
            # Atualiza quantidade do material
            material.quantidade_atual = nova_quantidade
            material.save()
            
            messages.success(request, 'Movimentação registrada com sucesso!')
            return redirect('detalhe_material', material_id=material.id)
    else:
        form = MovimentacaoForm()
    
    return render(request, 'materiais/form_movimentacao.html', {
        'form': form,
        'material': material
    })


@login_required
def relatorio_estoque(request):
    """Relatório completo do estoque"""
    materiais = Material.objects.filter(ativo=True).select_related('categoria')
    materiais = Material.objects.all()
    context = {
        'materiais': materiais,
    }
      
    # Filtros
    categoria_id = request.GET.get('categoria')
    if categoria_id:
        materiais = materiais.filter(categoria_id=categoria_id)
    
    # Cálculos
    valor_total_estoque = sum(m.valor_total_estoque for m in materiais)
    materiais_estoque_baixo = materiais.filter(quantidade_atual__lte=F('quantidade_minima'))
    
    categorias = Categoria.objects.all()
    
    context = {
        'materiais': materiais,
        'categorias': categorias,
        'categoria_selecionada': categoria_id,
        'valor_total_estoque': valor_total_estoque,
        'materiais_estoque_baixo': materiais_estoque_baixo,
    }
    return render(request, 'materiais/relatorio_estoque.html', context)

@login_required
def solicitacoes_compra(request):
    """Lista solicitações de compra"""
    solicitacoes = SolicitacaoCompra.objects.select_related('material', 'solicitante').order_by('-data_solicitacao')
    
    # Filtros
    status = request.GET.get('status')
    if status:
        solicitacoes = solicitacoes.filter(status=status)
    
    context = {
        'solicitacoes': solicitacoes,
        'status_selecionado': status,
    }
    return render(request, 'materiais/solicitacoes_compra.html', context)


@login_required
def nova_solicitacao_compra(request):
    """Cria nova solicitação de compra"""
    if request.method == 'POST':
        form = SolicitacaoCompraForm(request.POST)
        if form.is_valid():
            solicitacao = form.save(commit=False)
            solicitacao.solicitante = request.user
            solicitacao.save()
            messages.success(request, 'Solicitação de compra criada com sucesso!')
            return redirect('solicitacoes_compra')
    else:
        form = SolicitacaoCompraForm()
    
    return render(request, 'materiais/form_solicitacao.html', {'form': form})


@login_required
@require_POST
def aprovar_solicitacao(request, solicitacao_id):
    """Aprova ou rejeita uma solicitação de compra"""
    solicitacao = get_object_or_404(SolicitacaoCompra, id=solicitacao_id)
    
    data = json.loads(request.body)
    acao = data.get('acao')
    observacoes = data.get('observacoes', '')
    
    if acao in ['aprovada', 'rejeitada']:
        solicitacao.status = acao
        solicitacao.aprovador = request.user
        solicitacao.data_aprovacao = timezone.now()
        solicitacao.observacoes_aprovador = observacoes
        solicitacao.save()
        
        return JsonResponse({'success': True, 'message': f'Solicitação {acao} com sucesso!'})
    
    return JsonResponse({'success': False, 'message': 'Ação inválida'})

