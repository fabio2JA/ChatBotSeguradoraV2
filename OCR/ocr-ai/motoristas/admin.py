from django.contrib import admin
from .models import *

class CNHAdmin(admin.ModelAdmin):
    list_display = ['cpf', 'nome', 'numero_registro']
    search_fields = ['cpf', 'nome', 'numero_registro', 'validade', 'data_nascimento', 'data_emissao']
admin.site.register(CNH, CNHAdmin)

class DOCCarroAdmin(admin.ModelAdmin):
    list_display = ['cpf_ou_cnpj', 'nome', 'placa']
    search_fields = ['cpf_ou_cnpj', 'nome', 'cod_renavam', 'numero_crv', 
        'placa', 'ano_modelo', 'categoria', 'potencia', 'cod_seguranca_cla', 
        'modelo', 'tipo', 'data', 'local'                
    ]
admin.site.register(DOCCarro, DOCCarroAdmin)

admin.site.register(OCRQueue)

admin.site.register(DoneOCRQueue)
