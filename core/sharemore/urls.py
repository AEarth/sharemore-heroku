from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from core.views import (about, base, frontpage,  # FrontpageView, AboutView
                        styles)

urlpatterns = [

    path('about/', about, name='about'),
    path('admin/', admin.site.urls),
    path('base/', base, name='base'),
    path('', include('userprofile.urls')),
    path('', include('store.urls')),
    path('', frontpage, name='frontpage'),
    path('styles/', styles, name='styles'),
]

# if settings.enviro_set == 'local':
#     urlpatterns.insert(3, path("__debug__/", include("debug_toolbar.urls")),



#if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)