from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve as mediaserve


from django.urls import re_path as url
from django.views.static import serve


urlpatterns = [
    ##################################3
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    
    path('ashish/myadmin/admin', admin.site.urls),
    path('',include('mainapp.urls')),
    path('',include('sprintapp.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
