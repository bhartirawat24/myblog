from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()
from blogapp import views
from django.conf.urls.static import static
from django.conf import settings	

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('blogapp.urls'))   
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#/home/bhartirawat/blog/media/None/12239583_531599560327867_6108065189721824695_n.jpg