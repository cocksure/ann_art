import requests
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView

from .models import (
    MaterialItem, StyleItem, ProjectItem,
    ServiceItem, GuaranteeItem, InstallmentInfo, MaterialCategory, Partners
)

TELEGRAM_BOT_TOKEN = '7642436558:AAHGeHgE7wFrB7JVQpMBW172m6RLj_kV4UU'
TELEGRAM_GROUP_ID = '-1002713293259'


@csrf_exempt
def contact_telegram(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message_text = request.POST.get('message')  # описание проекта

        message = (
            "📩 Новое сообщение с сайта:\n\n"
            f"👤 Имя: {name}\n"
            f"📱 Телефон: {phone}\n"
            f"📝 Сообщение: {message_text}"
        )

        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {
            'chat_id': TELEGRAM_GROUP_ID,
            'text': message,
            'parse_mode': 'HTML'
        }

        response = requests.post(url, data=data)
        return JsonResponse({'ok': True})

    return JsonResponse({'error': 'Только POST-запрос разрешён'}, status=405)


def site_search(request):
    query = request.GET.get('q', '').strip()
    results = {}
    total = 0

    if query:
        # Поиск по ProjectItem
        projects = ProjectItem.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )

        # Поиск по ServiceItem
        services = ServiceItem.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )

        # Поиск по StyleItem
        styles = StyleItem.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )

        # Поиск по MaterialItem
        materials = MaterialItem.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        ).select_related('category')

        results = {
            'projects': projects,
            'services': services,
            'styles': styles,
            'materials': materials,
        }

        total = sum(len(qs) for qs in results.values())

    return render(request, 'site_search_results.html', {
        'query': query,
        'results': results,
        'total': total,
        'search_sections': [
            ('projects', _('Проекты')),
            ('services', _('Услуги')),
            ('styles', _('Стили')),
            ('materials', _('Материалы')),
            ('partners', _('Партнеры')),
        ]
    })


def home(request):
    return render(request, 'base.html', {
        "materials": MaterialItem.objects.order_by("order"),
        "styles": StyleItem.objects.order_by("order"),
        "projects": ProjectItem.objects.order_by("order"),
        "services": ServiceItem.objects.order_by("order"),
        "guarantees": GuaranteeItem.objects.order_by("order"),
        "installment": InstallmentInfo.objects.first(),
    })


class StyleItemView(ListView):
    model = StyleItem
    template_name = 'styles.html'
    context_object_name = 'styles'


class StyleItemDetailView(DetailView):
    model = StyleItem
    template_name = 'styles_detail.html'
    context_object_name = 'style'


class ServicesItemView(ListView):
    model = StyleItem
    template_name = 'base.html'
    context_object_name = 'services'


def material_category_list(request):
    categories = MaterialCategory.objects.all().order_by('order')
    return render(request, 'material_categories.html', {'material_categories': categories})


def projects_view(request):
    commercial = ProjectItem.objects.filter(category='commercial').order_by('order')
    residential = ProjectItem.objects.filter(category='residential').order_by('order')
    other = ProjectItem.objects.filter(category='other').order_by('order')

    return render(request, 'projects.html', {
        'commercial_projects': commercial,
        'residential_projects': residential,
        'other_projects': other,
    })


def project_detail(request, pk):
    project = get_object_or_404(ProjectItem, pk=pk)
    return render(request, 'project_detail.html', {'project': project})


def contacts(request):
    return render(request, 'contacts.html')


def materials_list(request):
    categories = MaterialCategory.objects.all()
    materials = MaterialItem.objects.select_related('category').all()

    # параметр из URL
    active_category_id = request.GET.get('category')
    try:
        active_category_id = int(active_category_id)
    except (TypeError, ValueError):
        # если не передали или невалидно → первая категория
        active_category_id = categories.first().id if categories.exists() else None

    context = {
        'categories': categories,
        'materials': materials,
        'partners': Partners.objects.all(),
        'active_category_id': active_category_id,
    }
    return render(request, 'materials_list.html', context)
