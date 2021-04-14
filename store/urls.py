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
  path('dashboard/', views.dashboard, name='dashboard')
]