"""infinitfolio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from portfolio.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('Error/', error),
    path('create/', create),
    path('<str:slug>/skills/', add_skill),
    path('<str:slug>/certs', add_certificate),
    path('<str:slug>/projects', add_project),
    path('certificate/<int:id>/delete', delete_certificate),
    path('skills/<int:id>/delete', delete_skill),
    path('projects/<int:id>/delete', delete_project),
    path('<str:slug>/work', add_work),
    path('work/<int:id>/delete', delete_work),
    path('<str:slug>/edit', edit_info),
    path('<str:slug>/delete', delete_website),
    path('<str:slug>/publish', publish),
    path('complete/', paymentComplete, name="complete"),
    path('<str:slug>/', display),
    path('<str:slug>/VPublish', publish_virtual),
    path('accounts/', include("Accounts.urls")),
    path('blogs/', include("blog.urls")),
    path('stores/', include("store.urls")),
    path('accounts/', include('django.contrib.auth.urls')),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
