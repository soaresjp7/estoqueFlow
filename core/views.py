import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, F, ExpressionWrapper, DecimalField
from .models import Produto
from .forms import ProdutoForm


def index(request):
    return render(request, 'core/index.html')

def sobre(request):
    return render(request, 'core/sobre.html')

def contato(request):
    return render(request, 'core/contato.html')


# Página pública: qualquer visitante pode ver os produtos
def produtos(request):
    lista_produtos = Produto.objects.all().order_by('nome')
    return render(request, 'core/produtos.html', {'produtos': lista_produtos})


# ---------- Dashboard ----------

ESTOQUE_BAIXO_LIMITE = 10
_valor_expr = ExpressionWrapper(F('quantidade') * F('preco'), output_field=DecimalField())

@login_required(login_url='login')
def dashboard(request):
    total_produtos = Produto.objects.count()

    valor_total = Produto.objects.aggregate(
        total=Sum(_valor_expr)
    )['total'] or 0

    estoque_baixo = Produto.objects.filter(
        quantidade__lt=ESTOQUE_BAIXO_LIMITE
    ).count()

    por_categoria = list(
        Produto.objects.values('categoria').annotate(
            count=Count('id'),
            valor=Sum(_valor_expr),
        ).order_by('-count')
    )

    dados_grafico = {
        'labels': [item['categoria'] or 'Sem categoria' for item in por_categoria],
        'counts': [item['count'] for item in por_categoria],
        'valores': [float(item['valor'] or 0) for item in por_categoria],
    }

    lista_produtos = Produto.objects.annotate(
        valor_item=ExpressionWrapper(F('quantidade') * F('preco'), output_field=DecimalField())
    ).order_by('quantidade', 'nome')

    return render(request, 'core/dashboard.html', {
        'total_produtos': total_produtos,
        'valor_total': float(valor_total),
        'estoque_baixo': estoque_baixo,
        'estoque_baixo_limite': ESTOQUE_BAIXO_LIMITE,
        'por_categoria': por_categoria,
        'dados_grafico': dados_grafico,
        'lista_produtos': lista_produtos,
    })


# ---------- Login / Logout ----------

def login_view(request):
    if request.user.is_authenticated:
        return redirect('admin_produtos')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin_produtos')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')

    return render(request, 'core/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


# ---------- CRUD de produtos (área administrativa) ----------

@login_required(login_url='login')
def admin_produtos(request):
    lista_produtos = Produto.objects.all().order_by('nome')
    return render(request, 'core/admin_produtos.html', {'produtos': lista_produtos})


@login_required(login_url='login')
def produto_criar(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto cadastrado com sucesso!')
            return redirect('admin_produtos')
    else:
        form = ProdutoForm()
    return render(request, 'core/produto_form.html', {'form': form, 'titulo': 'Novo Produto'})


@login_required(login_url='login')
def produto_editar(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto atualizado com sucesso!')
            return redirect('admin_produtos')
    else:
        form = ProdutoForm(instance=produto)
    return render(request, 'core/produto_form.html', {'form': form, 'titulo': 'Editar Produto'})


@login_required(login_url='login')
def produto_excluir(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        produto.delete()
        messages.success(request, 'Produto excluído com sucesso!')
        return redirect('admin_produtos')
    return render(request, 'core/produto_confirm_delete.html', {'produto': produto})
