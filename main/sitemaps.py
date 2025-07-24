from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import translation
from .models import ProjectItem, StyleItem

LANGUAGES = ['ru', 'en', 'uz']


class StaticPagesSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5
    protocol = "https"

    def items(self):
        return ['home', 'projects', 'styles', 'materials_list', 'contacts']

    def get_urls(self, site=None, **kwargs):
        urls = []
        for lang in LANGUAGES:
            with translation.override(lang):
                for item in self.items():
                    urls.append({
                        'location': f"{self.protocol}://{site.domain}{reverse(item)}",
                        'changefreq': self.changefreq,
                        'priority': self.priority,
                        'protocol': self.protocol,
                        'lastmod': None,
                    })
        return urls


class ProjectItemSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = "https"

    def items(self):
        return ProjectItem.objects.all()

    def get_urls(self, site=None, **kwargs):
        urls = []
        for lang in LANGUAGES:
            with translation.override(lang):
                for obj in self.items():
                    loc = reverse('project_detail', args=[obj.pk])
                    urls.append({
                        'location': f"{self.protocol}://{site.domain}{loc}",
                        'changefreq': self.changefreq,
                        'priority': self.priority,
                        'protocol': self.protocol,
                        'lastmod': None,
                    })
        return urls


class StyleItemSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = "https"

    def items(self):
        return StyleItem.objects.all()

    def get_urls(self, site=None, **kwargs):
        urls = []
        for lang in LANGUAGES:
            with translation.override(lang):
                for obj in self.items():
                    loc = reverse('style_detail', args=[obj.pk])
                    urls.append({
                        'location': f"{self.protocol}://{site.domain}{loc}",
                        'changefreq': self.changefreq,
                        'priority': self.priority,
                        'protocol': self.protocol,
                        'lastmod': None,
                    })
        return urls
