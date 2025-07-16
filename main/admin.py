from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from . import translation
from .models import (
    MaterialItem, StyleItem, ProjectItem,
    ServiceItem, MaterialCategory, Partners, MaterialImages, ProjectImages
)


@admin.register(MaterialCategory)
class MaterialCategoryAdmin(TranslationAdmin):
    list_display = ("name", 'description', 'image')
    list_editable = ('image',)
    group_fieldsets = True


@admin.register(MaterialItem)
class MaterialItemAdmin(TranslationAdmin):
    list_display = ("title", "order", 'description', 'image')
    ordering = ("order",)
    list_filter = ('category',)
    list_editable = ('image',)
    group_fieldsets = True


@admin.register(StyleItem)
class StyleItemAdmin(TranslationAdmin):
    list_display = ("title", 'description')
    ordering = ("order",)
    group_fieldsets = True


@admin.register(ProjectItem)
class ProjectItemAdmin(TranslationAdmin):
    list_display = ("title", 'square_meters', "order", 'category',)
    ordering = ("order",)
    list_filter = ('category',)
    group_fieldsets = True


@admin.register(ServiceItem)
class ServiceItemAdmin(admin.ModelAdmin):
    list_display = ("title", 'description', "order")
    ordering = ("order",)


@admin.register(Partners)
class PartnersAdmin(admin.ModelAdmin):
    list_display = ("id", "name", 'image')
    ordering = ("order",)
    list_editable = ('name', 'image')

admin.site.register(MaterialImages)
admin.site.register(ProjectImages)