from django.contrib import admin

from .models import (
    MaterialItem, StyleItem, ProjectItem,
    ServiceItem, GuaranteeItem, InstallmentInfo, MaterialCategory, Partners
)


@admin.register(MaterialCategory)
class MaterialCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", 'image')
    list_editable = ('image',)


@admin.register(MaterialItem)
class MaterialItemAdmin(admin.ModelAdmin):
    list_display = ("title", "order", 'description', 'image')
    ordering = ("order",)
    list_filter = ('category', )
    list_editable = ( 'image', )


@admin.register(StyleItem)
class StyleItemAdmin(admin.ModelAdmin):
    list_display = ("title", 'id', "order")
    ordering = ("order",)
    list_editable = ('order', )


@admin.register(ProjectItem)
class ProjectItemAdmin(admin.ModelAdmin):
    list_display = ("title", "order", 'category', )
    ordering = ("order",)
    list_filter = ('category', )


@admin.register(ServiceItem)
class ServiceItemAdmin(admin.ModelAdmin):
    list_display = ("title", "order")
    ordering = ("order",)

@admin.register(Partners)
class PartnersAdmin(admin.ModelAdmin):
    list_display = ("id", "name", 'image')
    ordering = ("order",)


