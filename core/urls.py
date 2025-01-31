from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from mainApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home'),
    path('bolim/<int:bolim_id>/', views.bolim_view, name='bolim'),
    path('mahsulot/<int:mahsulot_id>/sotish/', views.mahsulot_sotish, name='mahsulot_sotish'),
    path('statistika/', views.statistika_view, name='statistika'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)