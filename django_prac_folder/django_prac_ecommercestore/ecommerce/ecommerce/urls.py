"""
URL configuration for ecommerce project.

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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # In URL configuration, the namespace is used to organize URLs by application. 
    # It's a way to differentiate between URL names that might be the same across different apps 
    # within a Django project. By assigning a namespace to a set of URLs, we effectively create 
    # a scoped naming system for those URLs, which can be very useful in larger projects with 
    # multiple apps.
    path('', include('store.urls', namespace='store')),
]


"""
Q : Why use this if-statement?
A : When we see 'settings.py' in project folder at development level(before production),
    'DEBUG' is set to True. This tells django, if something gone wrong during development,
    display debug content(error message) on website. But in production level, in which website
    is deplyed, 'DEBUG' needs to be set False since nobody want user could see debugging messages
    when something gone wrong.
"""
if settings.DEBUG:
    # save images or media files to 'settings.MEDIA_ROOT', which are uploaded from admin site.
    urlpatterns += static(settings.MEDIA_URL, document=settings.MEDIA_ROOT)