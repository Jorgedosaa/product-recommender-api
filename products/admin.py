from django.contrib import admin

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("asin", "title", "category", "price", "created_at")
    search_fields = ("asin", "title", "description", "category")
    readonly_fields = ("embedding",)
