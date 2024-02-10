from django.contrib import admin
from .models import Category,Cart,CartItem,Product,UserProfile

admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Product)
admin.site.register(UserProfile)


