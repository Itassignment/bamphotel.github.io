from django.contrib import admin
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
  path('', home, name='home'),
  path('signup/', signup, name='signup'),
  path('login/', login, name='login'),
  path('logout/', logout, name='logout'),
  path('blog/', blog, name='blog'),
  path('delete/<int:id>', delete, name='delete'),
  ]
  
if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)