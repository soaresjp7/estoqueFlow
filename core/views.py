from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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
