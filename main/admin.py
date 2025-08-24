from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.sites.models import Site
from import_export.admin import ImportExportModelAdmin
from modeltranslation.admin import TranslationAdmin
from . import translation
# "from . import translation " shu turishi shart
from .models import (
    MaterialItem, StyleItem, ProjectItem,
    ServiceItem, MaterialCategory, Partners, MaterialImages, ProjectImages
)
from .resources import MaterialItemResource


@admin.register(MaterialCategory)
class MaterialCategoryAdmin(TranslationAdmin):
    list_display = ("name", 'id', 'order', 'description', 'image')
    list_editable = ('order', )
    group_fieldsets = True


@admin.register(MaterialItem)
class MaterialItemAdmin(ImportExportModelAdmin, TranslationAdmin):
    resource_class = MaterialItemResource
    list_display = ("title", "order", 'description', 'image')
    ordering = ("order",)
    list_filter = ('category',)
    list_editable = ('image', 'order', )
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
    list_display = ("id", 'title', "order")
    ordering = ("order",)


@admin.register(Partners)
class PartnersAdmin(admin.ModelAdmin):
    list_display = ("id", "name", 'image')
    ordering = ("order",)
    list_editable = ('name', 'image')

admin.site.register(MaterialImages)
admin.site.register(ProjectImages)

admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.unregister(Site)