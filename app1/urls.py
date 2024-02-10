from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path('',views.home,name='home'),
    path('login1', views.login1, name='login1'),
    path('registration', views.registration, name='registration'),
    path('admin', views.admin_dashboard, name='admin_dashboard'),
    path('add-category', views.add_category, name='add_category'),
    path('add-product', views.add_product, name='add_product'),
    path('show-products', views.show_products, name='show_products'),
    path('user-details', views.user_details, name='user_details'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('view_cart', views.view_cart, name='view_cart'),
    path('delete_from_cart/<int:item_id>/', views.delete_from_cart, name='delete_from_cart'),
    path('logout_view', views.logout_view, name='logout_view'),
    path('buyer', views.buyer, name='buyer'),
    path('categories/', views.categories, name='categories'),
    path('category/<int:category_id>/', views.category_products, name='category_products'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('profile/', views.user_profile, name='user_profile'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('deleteproduct', views.deleteproduct, name='deleteproduct'),



]



