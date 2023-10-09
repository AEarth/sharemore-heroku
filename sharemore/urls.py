from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from core.views import frontpage, about, base #FrontpageView, AboutView

urlpatterns = [
    path("__debug__/", include("debug_toolbar.urls")),
    path('about/', about, name='about'),
    path('admin/', admin.site.urls),
    path('base/', base, name='base'),
    path('', include('userprofile.urls')),
    path('', include('store.urls')),
    path('', frontpage, name='frontpage'),


]
#if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)