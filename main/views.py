from django.shortcuts import render

from .models import (
    MaterialItem, StyleItem, ProjectItem,
    ServiceItem, GuaranteeItem, InstallmentInfo
)


def home(request):
    return render(request, 'index.html', {
        "materials": MaterialItem.objects.order_by("order"),
        "styles": StyleItem.objects.order_by("order"),
        "projects": ProjectItem.objects.order_by("order"),
        "services": ServiceItem.objects.order_by("order"),
        "guarantees": GuaranteeItem.objects.order_by("order"),
        "installment": InstallmentInfo.objects.first(),
    })
