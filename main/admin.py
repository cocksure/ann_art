from django.contrib import admin
from .models import (
    MaterialItem, StyleItem, ProjectItem,
    ServiceItem, GuaranteeItem, InstallmentInfo
)

@admin.register(MaterialItem)
class MaterialItemAdmin(admin.ModelAdmin):
    list_display = ("title", "order")
    ordering = ("order",)

@admin.register(StyleItem)
class StyleItemAdmin(admin.ModelAdmin):
    list_display = ("title", "order")
    ordering = ("order",)

@admin.register(ProjectItem)
class ProjectItemAdmin(admin.ModelAdmin):
    list_display = ("title", "order")
    ordering = ("order",)

@admin.register(ServiceItem)
class ServiceItemAdmin(admin.ModelAdmin):
    list_display = ("title", "order")
    ordering = ("order",)

@admin.register(GuaranteeItem)
class GuaranteeItemAdmin(admin.ModelAdmin):
    list_display = ("title", "order")
    ordering = ("order",)

@admin.register(InstallmentInfo)
class InstallmentInfoAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Разрешить только 1 объект
        return not InstallmentInfo.objects.exists()