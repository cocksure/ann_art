from modeltranslation.translator import register, TranslationOptions

from .models import MaterialCategory, MaterialItem, StyleItem, ProjectItem, ServiceItem


@register(MaterialCategory)
class MaterialCategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(MaterialItem)
class MaterialItemTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(StyleItem)
class StyleItemTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(ProjectItem)
class ProjectItemTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(ServiceItem)
class ServiceItemTranslationOptions(TranslationOptions):
    fields = ('title', 'description')