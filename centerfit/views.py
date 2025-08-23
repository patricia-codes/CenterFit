from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CheckoutForm, UserRegisterForm, UserUpdateForm
from .models import (
  Carrinho,
  Categoria,
  Compra,
  ItemCarrinho,
  Marca,
  Produto,
)


# Create your views here.
def index(request):
  produtos = Produto.objects.all()
  marcas = Marca.objects.all()
  produtos_recentes = Produto.objects.order_by('-created_at')[:4]
  return render(request, 'index.html', {'produtos': produtos, 
                                        'marcas': marcas,
                                        'produtos_recentes': produtos_recentes})

def adicionar_ao_carrinho(request, produto_id):
  produto = get_object_or_404(Produto, id=produto_id)
  quantidade = int(request.POST.get("quantidade", 1))
  # pega ou cria carrinho do usuário
  carrinho, _ = Carrinho.objects.get_or_create(usuario=request.user)
  # tenta achar item já existente
  item, criado = ItemCarrinho.objects.get_or_create(
    carrinho=carrinho,
    produto=produto,
    defaults={'quantidade': quantidade}
  )
  if not criado:
      item.quantidade += quantidade
      item.save()
  return redirect("carrinho")

def buscar(request):
  termo = request.GET.get('termo')
  produtos = Produto.objects.filter(nome__icontains=termo)
  if produtos:
    return render(request, 'produtos.html', {'produtos': produtos})
  return render(request, 'produtos.html', {'produtos': []})

def cadastro(request):
  if request.method == 'POST':
    form = UserRegisterForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
  else:
    form = UserRegisterForm()
  return render(request, 'registration/cadastro.html', {'form': form})

def carrinho(request):
  carrinho, _ = Carrinho.objects.get_or_create(usuario=request.user)
  itens = carrinho.itens.all()
  total = carrinho.total()
  return render(request, "carrinho.html", {"carrinho": carrinho, 
                                           "itens": itens, "total": total})

def remover_item(request, item_id):
  item = ItemCarrinho.objects.get(id=item_id, carrinho__usuario=request.user)
  item.delete()
  return redirect("carrinho")

def atualizar_quantidade(request, item_id):
  item = ItemCarrinho.objects.get(id=item_id, carrinho__usuario=request.user)
  if request.method == "POST":
    nova_qtd = int(request.POST.get("quantidade", 1))
    if nova_qtd > 0:
        item.quantidade = nova_qtd
        item.save()
    else:
        item.delete()
  return redirect("carrinho")

def checkout(request):
  carrinho, _ = Carrinho.objects.get_or_create(usuario=request.user)

  if request.method == "POST":
    form = CheckoutForm(request.POST)
    if form.is_valid():
      endereco = form.cleaned_data["endereco"]
      forma_pagamento = form.cleaned_data["forma_pagamento"]
      try:
        pedido = Compra.checkout(carrinho, endereco, forma_pagamento)
        return redirect("detalhes_pedido", pedido_id=pedido.id)
      except ValueError as e:
        messages.error(request, str(e))
        return redirect("carrinho")
  else:
      form = CheckoutForm()

  return render(request, "checkout.html", {"form": form, "carrinho": carrinho})

def compra(request, compra_id):
  compra = get_object_or_404(Compra, id=compra_id, usuario=request.user)
  return render(request, "compra.html", {"compra": compra})

def contato(request):
  return render(request, 'contato.html')

def detalhes_pedido(request, pedido_id):
  pedido = Compra.objects.get(id=pedido_id, usuario=request.user)
  return render(request, "detalhes_pedido.html", {"pedido": pedido})

def login_modal_view(request):
  if request.method == "POST":
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
      login(request, user)
      #volta pra página
      return JsonResponse({"success": True})  
    else:
      return JsonResponse({"success": False, "error": "Usuário ou senha inválidos."})

def logout_view(request):
  logout(request)
  return redirect('index')

def pedidos(request):
  pedidos  = Compra.objects.filter(usuario=
                                  request.user).order_by("-criado_em").prefetch_related("itens__produto")
  return render(request, "pedidos.html", {"pedidos": pedidos})

def perfil(request):
  user = request.user
  if request.method == 'POST':
    if 'delete_account' in request.POST:
      user.delete()
      messages.success(request, "Sua conta foi deletada com sucesso.")
      return redirect('/')
    form = UserUpdateForm(request.POST, instance=request.user)
    if form.is_valid():
      user = form.save()
      update_session_auth_hash(request, user)
      messages.success(request, "Seus dados foram atualizados com sucesso!")
      return redirect('perfil')
  else:
    form = UserUpdateForm(instance=request.user)
  return render(request, 'perfil.html', {'form': form})

def privacidade(request):
  return render(request, 'privacidade.html')

def produto(request, slug):
  produto = get_object_or_404(Produto, slug=slug)
  return render(request, 'produto.html', {'produto': produto})

def filtrar_produtos_por_categorias(queryset, categorias):
  if not categorias:
      return queryset
  # Filtra produtos que têm categorias dentro da lista
  queryset = queryset.filter(categorias__nome__in=categorias)

  # Conta quantas das categorias selecionadas cada produto tem
  queryset = queryset.annotate(
    num_categorias=Count('categorias')).filter(num_categorias__gte=len(categorias))
  return queryset.distinct()

def produtos(request):
  produtos = Produto.objects.all()
  # Filtros múltiplos
  marcas = request.GET.getlist('marca')
  categorias = request.GET.getlist("categoria")
  if marcas:
    produtos = produtos.filter(marca__nome__in=marcas)
  if categorias:
    produtos = filtrar_produtos_por_categorias(produtos, categorias)
  context = {
    'marcas': Marca.objects.all(),
    'categorias': Categoria.objects.all(),
    'produtos': produtos
  }
  return render(request, 'produtos.html', context)

def sobre(request):
  return render(request, 'sobre.html')

def trocas(request):
  return render(request, 'trocas.html')