import os
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from motoristas.views import home, reconhecimento_cnh, reconhecimento_doc, verify_done_ocr


urlpatterns = [
    path(os.environ.get('ADMIN_URL'), admin.site.urls),
    path('', home, name='home_view'),

    path('reconhecimento/cnh/', reconhecimento_cnh, name='reconhecimento_cnh_view'),

    path('reconhecimento/doc/', reconhecimento_doc, name='reconhecimento_doc_view'),

    path('ocr-status/', verify_done_ocr, name='verify_ocr_status_view')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
