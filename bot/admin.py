from django.contrib import admin

from bot.models import Branch, Categories, Product


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_filter = ['title']
    search_fields = ['title']
    list_display = ['title']

@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_filter = ['title']
    search_fields = ['title']
    list_display = ['title']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_filter = ['title']
    search_fields = ['title']
    list_display = ['title']