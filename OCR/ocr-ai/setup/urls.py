import os
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from motoristas.views import home, reconhecimento_cnh, reconhecimento_doc, verify_done_ocr, reconhecimento_bot_doc, reconhecimento_bot_cnh


urlpatterns = [
    path('reconhecimento/cnh/bot/', reconhecimento_bot_cnh, name='reconhecimento_bot_cnh_view'),
    path('reconhecimento/doc/bot/', reconhecimento_bot_doc, name='reconhecimento_bot_doc_view'),
    
    path(os.environ.get('ADMIN_URL'), admin.site.urls),

    path('', home, name='home_view'),

    path('reconhecimento/cnh/', reconhecimento_cnh, name='reconhecimento_cnh_view'),

    path('reconhecimento/doc/', reconhecimento_doc, name='reconhecimento_doc_view'),

    path('ocr-status/', verify_done_ocr, name='verify_ocr_status_view'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
