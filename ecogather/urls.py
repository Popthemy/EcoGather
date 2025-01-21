"""
URL configuration for ecogather project.

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
from django.contrib import admin
from django.urls import path,include
from debug_toolbar.toolbar import debug_toolbar_urls

# Adding images
from django.conf import settings
from django.conf.urls.static import static

# for documentation
from drf_spectacular.views import SpectacularAPIView,SpectacularSwaggerView

admin.site.index_title = 'Green Admin'
admin.site.site_header = 'EcoGather: A Greener Way to Event Planning'


# Version 1 URLs
first_version = [
    path('users/', include('myuser.urls')),
    path('', include('greenplan.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('playground/', include('myutils.urls')),
    path('api/v1/', include(first_version)),
    path('', include('frontend_demo.urls')),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/',
         SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

] + debug_toolbar_urls()

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if settings.DEBUG:
    #adding image url only in production
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
