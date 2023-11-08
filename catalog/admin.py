from django.contrib import admin

from catalog.models import Category, Product, Organization, Version


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name',)
    ordering = ('pk',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'price', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'description')
    ordering = ('-pk',)


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'phone', 'email')


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ('name', 'product', 'is_active')
    