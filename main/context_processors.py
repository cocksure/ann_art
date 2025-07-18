from .models import MaterialCategory


def material_categories(request):
    return {
        'footer_material_categories': MaterialCategory.objects.all().order_by('order')
    }
