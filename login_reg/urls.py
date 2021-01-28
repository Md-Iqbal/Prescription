
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls'), name='prescription'),
    path('patient/', include('patient.urls'), name='patient'),
    path('message/', include('message_app.urls'), name='messaging'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
