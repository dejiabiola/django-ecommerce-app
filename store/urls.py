from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('cart/', views.cart, name='cart'),
  path('checkout/', views.checkout, name='checkout'),
  path('login/', views.user_login, name='login'),
  path('register/', views.register, name='register'),
  path('logout/', views.logoutUser, name='logout'),
  path('product/<int:id>/', views.product_detail, name= 'product_detail'),
  path('dashboard/', views.dashboard, name='dashboard'),
  path('product/buy/', views.product_buy, name='product_buy'),
  path('product/<int:id>/edit/', views.product_edit, name= 'product_edit'),
  path('product/<int:id>/delete/', views.product_delete, name= 'product_delete'),
  path('product_new/', views.product_new, name= 'product_new'),
]