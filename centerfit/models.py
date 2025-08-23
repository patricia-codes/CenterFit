from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


class Perfil(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  cpf = models.CharField(max_length=20, unique=True)
  def __str__(self):
    return str(self.cpf)

class Categoria(models.Model):
  nome = models.CharField(max_length=50, unique=True)
  def __str__(self):
    return str(self.nome)

class Marca(models.Model):
  nome = models.CharField(max_length=50, unique=True)
  imagem = models.ImageField(upload_to='marcas/')
  def __str__(self):
    return str(self.nome)

class Produto(models.Model):
  nome = models.CharField(max_length=200)
  slug = models.SlugField(unique=True, blank=True)
  preco = models.DecimalField(max_digits=10, decimal_places=2)
  descricao = models.TextField()
  estoque = models.PositiveIntegerField()
  created_at = models.DateTimeField(auto_now_add=True)
  # relacionamentos
  categorias = models.ManyToManyField(Categoria, blank=True, related_name='produtos')
  marca = models.ForeignKey(Marca, blank=True, on_delete=models.SET_NULL, null=True, 
                            related_name='produtos')

  def __str__(self):
    return str(self.nome)

  def save(self, *args, **kwargs):
    # Sempre atualiza o slug
    base_slug = slugify(self.nome)
    slug = base_slug
    num = 1
    # Garante que o slug seja único
    while Produto.objects.filter(slug=slug).exclude(pk=self.pk).exists():
      slug = f"{base_slug}-{num}"
      num += 1
    self.slug = slug
    super().save(*args, **kwargs)

class ProdutoImagem(models.Model):
  produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name="imagens")
  imagem = models.ImageField(upload_to="produtos/")
  def __str__(self):
      return f"Imagem de {self.produto.nome}"

  # --- Carrinho ---
class Carrinho(models.Model):
  usuario = models.OneToOneField(User,on_delete=models.CASCADE,related_name='carrinho')
  criado_em = models.DateTimeField(auto_now_add=True)
  def __str__(self):
    return f"Carrinho de ({self.usuario.first_name})"
  def total(self):
    return sum(item.subtotal for item in self.itens.all())

class ItemCarrinho(models.Model):
  carrinho = models.ForeignKey(Carrinho, on_delete=models.CASCADE, related_name="itens")
  produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
  quantidade = models.PositiveIntegerField(default=1)
  def __str__(self):
    return f"{self.quantidade} x {self.produto.nome}"
  @property
  def subtotal(self):
    return self.produto.preco * self.quantidade

# --- Compra Efetuada ---
class Compra(models.Model):
  FORMAS_PAGAMENTO = [
      ('boleto', 'Boleto'),
      ('cartao', 'Cartão de Crédito'),
      ('pix', 'PIX'),
  ]
  usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='compras')
  criado_em = models.DateTimeField(auto_now_add=True)
  endereco = models.CharField(max_length=200)
  pagamento = models.CharField(max_length=20, choices=FORMAS_PAGAMENTO)
  def __str__(self):
    return f"Compra {self.id} by {self.usuario.username}"
  def total(self):
    return sum(item.subtotal for item in self.itens.all())
  @classmethod
  def checkout(cls, carrinho, endereco, forma_pagamento):
    pedido = cls.objects.create(
      usuario=carrinho.usuario,
      endereco=endereco,
      pagamento=forma_pagamento
    )
    for item in carrinho.itens.all():
      if item.produto.estoque < item.quantidade:
        raise ValueError(f"Estoque insuficiente para {item.produto.nome}")
      item.produto.estoque -= item.quantidade
      item.produto.save()

      ItemCompra.objects.create(
          compra=pedido,
          produto=item.produto,
          quantidade=item.quantidade,
          preco_unitario=item.produto.preco
      )
    carrinho.itens.all().delete()
    return pedido

class ItemCompra(models.Model):
  compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name="itens")
  produto = models.ForeignKey(Produto, on_delete=models.SET_NULL, null=True)
  quantidade = models.PositiveIntegerField()
  preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)
  def __str__(self):
    return f"{self.quantidade} x {self.produto.nome}"
  @property
  def subtotal(self):
    return self.preco_unitario * self.quantidade