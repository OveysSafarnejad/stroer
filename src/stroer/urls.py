"""
URL configuration for stroer project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from apps.post.urls import (
    comment_router,
    post_router,
)

schema_view = get_schema_view(
   openapi.Info(
      title="Stroer rest application",
      default_version='v1',
      description="A simple drf project for training",
      terms_of_service="",
      contact=openapi.Contact(email="safarnejad.ho@gmail.com"),
      license=openapi.License(name=""),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0),
            name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0),
            name='schema-redoc'),
    path('api-auth/', include('rest_framework.urls')),
    path('auth/', include('apps.user.urls'), name='authentication'),

    path('', include((post_router.urls, 'posts'))),
    path('', include((comment_router.urls, 'comments'))),
]

if settings.DEBUG:
    urlpatterns += [re_path(r'^admin/', admin.site.urls)]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    urlpatterns += [re_path(settings.ADMIN_URL, admin.site.urls)]
