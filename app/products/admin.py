from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin

from .models import Category, Product, Order, SelectedProduct


class SelectedProductInline(admin.TabularInline):
    model = SelectedProduct
    extra = 0


@admin.register(Category)
class CategoryAdmin(TabbedTranslationAdmin):
    list_display = ['name_uz', 'name_ru', 'is_active']


@admin.register(Product)
class ProductAdmin(TabbedTranslationAdmin):
    list_display = ['name_uz', 'name_ru', 'price', 'is_active']
    list_filter = ['category']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['filial', 'address', 'user_phone', 'all_cost', 'delivery', "status"]
    list_display_links = ['filial', 'address', 'user_phone']
    inlines = [SelectedProductInline]

    def user_phone(self, obj):
        return obj.user.phone if obj.user else None

    user_phone.short_description = 'Telefon raqam'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')
