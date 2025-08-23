from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from centerfit import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('adicionar/<int:produto_id>/', views.adicionar_ao_carrinho, 
         name='adicionar_ao_carrinho'),
    path('buscar/', views.buscar, name="buscar"),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('carrinho/', views.carrinho, name='carrinho'),
    path("carrinho/remover/<int:item_id>/", views.remover_item, 
         name="remover_item"),
    path("carrinho/atualizar/<int:item_id>/", views.atualizar_quantidade,
         name="atualizar_quantidade"),
    path('checkout/', views.checkout, name='checkout'),
    path('compra/<int:compra_id>/', views.compra, name='compra'),
    path('contato/', views.contato, name='contato'),
    path('detalhes_pedido/<int:pedido_id>/', views.detalhes_pedido, 
         name='detalhes_pedido'),
    path('login/', views.login_modal_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('pedidos', views.pedidos, name='pedidos'),
    path('perfil/', views.perfil, name='perfil'),
    path('privacidade/', views.privacidade, name='privacidade'),
    path('produto/<slug:slug>/', views.produto, 
     name="produto"),
    path('produtos', views.produtos, name="produtos"),
    path('sobre/', views.sobre, name='sobre'),
    path('trocas/', views.trocas, name='trocas'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)