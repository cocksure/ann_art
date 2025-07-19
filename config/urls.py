from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.i18n import set_language
from django.contrib.sitemaps.views import sitemap

from main.sitemaps import ProjectItemSitemap, MaterialItemSitemap, ServiceItemSitemap, StyleItemSitemap

sitemaps = {
    'projects': ProjectItemSitemap,
    'materials': MaterialItemSitemap,
    'services': ServiceItemSitemap,
    'styles': StyleItemSitemap,
}

urlpatterns = [
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('set-language/', set_language, name='set_language'),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
