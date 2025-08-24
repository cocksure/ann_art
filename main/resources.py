# app/resources.py
from import_export import resources, fields
from import_export.widgets import Widget
from django.core.exceptions import ValidationError
from .models import MaterialItem, MaterialCategory

class CategoryIdWidget(Widget):
    def clean(self, value, row=None, *args, **kwargs):
        try:
            pk = int(float(value))  # Excel часто даёт "1.0"
            return MaterialCategory.objects.get(pk=pk)
        except (ValueError, TypeError):
            raise ValidationError(f"Некорректный category_id: {value}")
        except MaterialCategory.DoesNotExist:
            raise ValidationError(f"Категория с id={value} не найдена.")

    def render(self, value, obj=None):
        return value.pk if value else ""

class MaterialItemResource(resources.ModelResource):
    category = fields.Field(
        attribute='category',
        column_name='category_id',
        widget=CategoryIdWidget(),
    )

    title_ru = fields.Field(attribute='title_ru', column_name='title_ru')
    title_en = fields.Field(attribute='title_en', column_name='title_en')
    title_uz = fields.Field(attribute='title_uz', column_name='title_uz')

    description_ru = fields.Field(attribute='description_ru', column_name='description_ru')
    description_en = fields.Field(attribute='description_en', column_name='description_en')
    description_uz = fields.Field(attribute='description_uz', column_name='description_uz')

    class Meta:
        model = MaterialItem
        import_id_fields = ['title_ru']  # лучше завести slug
        fields = (
            'category',
            'title_ru', 'title_en', 'title_uz',
            'description_ru', 'description_en', 'description_uz',
        )
        skip_unchanged = True
        report_skipped = True