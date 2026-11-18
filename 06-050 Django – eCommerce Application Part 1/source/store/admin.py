from django.contrib import admin
from .models import Store, Product, Review, ResetToken


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner')
    search_fields = ('name', 'owner__username')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'store', 'price', 'stock')
    list_filter = ('store',)
    search_fields = ('name', 'store__name')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'author', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')


@admin.register(ResetToken)
class ResetTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'expiry_date', 'used')
    list_filter = ('used',)
