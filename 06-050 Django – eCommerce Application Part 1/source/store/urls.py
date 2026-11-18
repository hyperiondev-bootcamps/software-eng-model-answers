from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    # Marketplace & Product Views
    path('', views.home, name='home'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('products/<int:product_id>/review/', views.add_review, name='add_review'),

    # Authentication & User Management
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),

    # Password reset routes
    path('password_reset/', views.send_password_reset, name='password_reset_request'),
    path('reset_password/<str:token>/', views.reset_user_password, name='password_reset'),

    # Shopping Cart & Checkout (Session-based)
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:product_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),

    # Vendor Management Views
    path('dashboard/', views.vendor_dashboard, name='vendor_dashboard'),
    path('store/create/', views.create_store, name='create_store'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/<int:product_id>/edit/', views.edit_product, name='edit_product'),
    path('products/<int:product_id>/delete/', views.delete_product, name='delete_product'),
]

