from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import ProjectItem, StyleItem


class StaticPagesSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5
    protocol = "https"

    def items(self):
        return ['home', 'projects', 'styles', 'materials_list', 'contacts']

    def location(self, item):
        return reverse(item)


class ProjectItemSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = "https"

    def items(self):
        return ProjectItem.objects.all()

    def location(self, obj):
        return reverse('project_detail', args=[obj.pk])


class StyleItemSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = "https"

    def items(self):
        return StyleItem.objects.all()

    def location(self, obj):
        return reverse('style_detail', args=[obj.pk])