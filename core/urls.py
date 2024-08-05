
from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include, re_path
from django.views.static import serve
from django.views.generic import TemplateView
from core.settings import ENVIRONMENT, MEDIA_ROOT, STATIC_ROOT


def handler404(request, *args, **kwargs):
    return render(request, "404.html")


def handler500(request, *args, **kwargs):
    return render(request, "500.html")


# EXTERNAL APPS URLS
urlpatterns = [

    # DJANGO URLS > remove in extreme security
    path('admin/', admin.site.urls),

    # API URLS
    path('accounts/', include('allauth.urls')),

]

# universal urls
urlpatterns += [
    path('under-construction/', TemplateView.as_view(template_name='000.html')),

]

# your apps urls
urlpatterns += [
    # path('', include('src.website.urls', namespace='website')),
    path('accounts/', include('src.accounts.urls', namespace='accounts')),
    path('admins/', include('src.administration.admins.urls', namespace='admins')),
    path('', include('src.website.urls', namespace='website')),
    path('c/', include('src.administration.client.urls', namespace='client')),
]

urlpatterns += [
    path('tinymce/', include('tinymce.urls')),
]

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),
]

if ENVIRONMENT != 'server':
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls"))
    ]
