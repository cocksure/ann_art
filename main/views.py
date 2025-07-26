import time

import requests
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.utils.translation import get_language
from django.utils.translation import gettext as _
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, DetailView

from .models import (
    MaterialItem, StyleItem, ProjectItem,
    ServiceItem, GuaranteeItem, InstallmentInfo, MaterialCategory, Partners
)

TELEGRAM_BOT_TOKEN = '7642436558:AAHGeHgE7wFrB7JVQpMBW172m6RLj_kV4UU'
TELEGRAM_GROUP_ID = '-1002713293259'


@csrf_protect
def contact_telegram(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Только POST-запрос разрешён'}, status=405)

    # Honeypot — если поле заполнено, скорее всего бот
    if request.POST.get('company'):
        return JsonResponse({'ok': True})  # тихо игнорируем

    # Проверка времени заполнения
    try:
        form_ts = int(request.POST.get('form_ts', '0'))
    except ValueError:
        form_ts = 0
    if form_ts and time.time() - form_ts < 2:
        return JsonResponse({'error': 'Слишком быстро отправлено. Попробуйте снова.'}, status=400)

    # Получаем данные
    name = (request.POST.get('name') or '').strip()
    phone = (request.POST.get('phone') or '').strip()
    message_text = (request.POST.get('message') or '').strip()

    # Валидация
    if not name or len(name) > 25:
        return JsonResponse({'error': 'Некорректное имя.'}, status=400)
    if not phone.isdigit() or len(phone) != 9:
        return JsonResponse({'error': 'Некорректный номер телефона.'}, status=400)
    if len(message_text) > 1000:
        message_text = message_text[:1000]

    # Формируем сообщение
    message = (
        "📩 Новое сообщение с сайта:\n\n"
        f"👤 Имя: {name}\n"
        f"📱 Телефон: +998 {phone}\n"
        f"📝 Сообщение: {message_text}"
    )

    # Отправка в Telegram
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        'chat_id': TELEGRAM_GROUP_ID,
        'text': message,
        'parse_mode': 'HTML'
    }

    try:
        requests.post(url, data=data, timeout=5)
    except Exception as e:
        return JsonResponse({'error': 'Ошибка отправки. Попробуйте позже.'}, status=500)

    return JsonResponse({'ok': True})


def site_search(request):
    query = request.GET.get('q', '').strip()
    results = {}
    total = 0

    if query:
        query_lower = query.lower()
        current_language = get_language()

        def search_queryset(model, select_related=None):
            # Для русского языка оставляем как было
            if current_language == 'ru':
                vector = SearchVector('title', 'description', config='russian')
                search_query = SearchQuery(query_lower, config='russian')
                similarity_field = 'title'
            # Для других языков используем соответствующие поля
            else:
                title_field = f'title_{current_language}'
                desc_field = f'description_{current_language}'
                vector = SearchVector(title_field, desc_field, config='simple')
                search_query = SearchQuery(query_lower, config='simple')
                similarity_field = title_field

            qs = model.objects.annotate(
                search=vector,
                rank=SearchRank(vector, search_query),
                similarity=TrigramSimilarity(similarity_field, query_lower)
            ).filter(
                Q(search=search_query) |
                Q(similarity__gt=0.1)
            ).order_by('-rank', '-similarity')

            if select_related:
                qs = qs.select_related(*select_related)
            return qs

        projects = search_queryset(ProjectItem)
        services = search_queryset(ServiceItem)
        styles = search_queryset(StyleItem)
        materials = search_queryset(MaterialItem, select_related=['category'])

        results = {
            'projects': projects,
            'services': services,
            'styles': styles,
            'materials': materials,
        }

        total = sum(qs.count() for qs in results.values())

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


def custom_404(request, exception):
    return render(request, '404.html', status=404)
