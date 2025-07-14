import requests
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView

from .models import (
    MaterialItem, StyleItem, ProjectItem,
    ServiceItem, GuaranteeItem, InstallmentInfo, MaterialCategory, Partners
)


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


def material_items_by_category(request, category_id):
    category = get_object_or_404(MaterialCategory, id=category_id)
    items = MaterialItem.objects.filter(category=category).order_by('order')
    partners = Partners.objects.all()
    return render(request, 'products.html', {
        'category': category,
        'items': items,
        'partners': partners
    })

def products(request):
    return render(request, 'products.html')


def projects(request):
    return render(request, 'projects.html')


def contacts(request):
    return render(request, 'contacts.html')


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
