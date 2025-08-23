from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html

from .models import (
  Carrinho,
  Categoria,
  Compra,
  ItemCarrinho,
  ItemCompra,
  Marca,
  Perfil,
  Produto,
  ProdutoImagem,
)


# Register your models here.
class ProfileInline(admin.StackedInline):
  model = Perfil
  can_delete = False

# apaga o user normal e cria um novo com perfil para mostrar o cpf
class UserAdminWithProfile(UserAdmin):
  inlines = [ProfileInline]
  list_display = ('id', 'username', 'first_name', 'last_name', 'get_cpf', 'is_staff')
  search_fields = ('username', 'cpf', 'first_name', 'last_name')
  def get_cpf(self, obj):
    return obj.perfil.cpf if hasattr(obj, "perfil") else ""

admin.site.unregister(User)
admin.site.register(User, UserAdminWithProfile)

# --- PRODUTOS ---
class ProdutoImagemInline(admin.TabularInline):
    model = ProdutoImagem
    extra = 1
    #Preview da imagem no admin
    readonly_fields = ('imagem_preview',)

    def imagem_preview(self, obj):
        if obj.imagem:
            return format_html('<img src="{}" style="width: 100px; height:auto;" />', 
                               obj.imagem.url)
        return "-"
    imagem_preview.short_description = 'Preview'

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'marca', 'preco', 'estoque', 'slug')
    search_fields = ('nome',)
    list_filter = ('marca', 'categorias')
    inlines = [ProdutoImagemInline]
    filter_horizontal = ('categorias',)
    # Preview da primeira imagem
    def imagem_principal_preview(self, obj):
        primeira_imagem = obj.imagens.first()
        if primeira_imagem and primeira_imagem.imagem:
            return format_html('<img src="{}" style="width: 60px; height:auto;" />', 
                               primeira_imagem.imagem.url)
        return "-"
    imagem_principal_preview.short_description = 'Imagem'

@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    search_fields = ('nome',)

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    search_fields = ('nome',)

# --- CARRINHO ---
class ItemCarrinhoInline(admin.TabularInline):
    model = ItemCarrinho
    extra = 0
    readonly_fields = ('subtotal',)

@admin.register(Carrinho)
class CarrinhoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'criado_em', 'total')
    inlines = [ItemCarrinhoInline]

# --- COMPRA ---
class ItemCompraInline(admin.TabularInline):
    model = ItemCompra
    extra = 0
    readonly_fields = ('subtotal', 'preco_unitario')

@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'pagamento', 'criado_em', 'total')
    list_filter = ('pagamento', 'criado_em')
    search_fields = ('usuario__username',)
    inlines = [ItemCompraInline]