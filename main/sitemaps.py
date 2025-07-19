from django.contrib.sitemaps import Sitemap
from .models import ProjectItem, MaterialItem, ServiceItem, StyleItem


class ProjectItemSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return ProjectItem.objects.all()

    def lastmod(self, obj):
        return obj.updated_at if hasattr(obj, 'updated_at') else None


class MaterialItemSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return MaterialItem.objects.all()

    def lastmod(self, obj):
        return obj.updated_at if hasattr(obj, 'updated_at') else None


class ServiceItemSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return ServiceItem.objects.all()


class StyleItemSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return StyleItem.objects.all()

    def lastmod(self, obj):
        return obj.updated_at if hasattr(obj, 'updated_at') else None