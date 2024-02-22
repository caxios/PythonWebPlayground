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
    
    path('basket/', include('basket.urls', namespace='basket')),
    path('account/', include('account.urls', namespace='account')),
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
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)