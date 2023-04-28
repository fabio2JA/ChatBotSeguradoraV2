from django.db import models
from django.utils import timezone
from encrypted_fields import fields

from motoristas.constants import IMAGE_TYPE_CHOICES


class CNH(models.Model):
    numero_cel = fields.EncryptedCharField(max_length=25)
    image = models.ImageField()
    cpf = fields.EncryptedCharField(max_length=14, null=False, blank=False, primary_key=True)
    nome = fields.EncryptedCharField(max_length=255, blank=True, null=True)
    documento = fields.EncryptedCharField(max_length=75, blank=True, null=True)
    data_nascimento = fields.EncryptedCharField(max_length=25, blank=True, null=True)
    validade = fields.EncryptedCharField(max_length=25, blank=True, null=True)
    numero_registro = fields.EncryptedCharField(max_length=20, blank=True, null=True)
    data_primeira_habilitacao = fields.EncryptedCharField(max_length=25, blank=True, null=True)
    permissao = fields.EncryptedCharField(max_length=15, blank=True, null=True)
    acc = fields.EncryptedCharField(max_length=15, blank=True, null=True)
    categoria = fields.EncryptedCharField(max_length=3, blank=True, null=True)
    data_emissao = fields.EncryptedCharField(max_length=25, blank=True, null=True)
    local = fields.EncryptedCharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'{self.nome} - {self.cpf}'


class DOCCarro(models.Model):
    numero_cel = fields.EncryptedCharField(max_length=25)
    image = models.ImageField()
    cpf_ou_cnpj = fields.EncryptedCharField(max_length=20, blank=True, null=True)
    nome = fields.EncryptedCharField(max_length=255, blank=True, null=True)

    # COL 1
    cod_renavam = fields.EncryptedCharField(max_length=20, blank=True, null=True)
    placa = fields.EncryptedCharField(max_length=7, blank=True, null=True)
    exercicio = fields.EncryptedCharField(max_length=10, blank=True, null=True)
    ano_fabricacao = fields.EncryptedCharField(max_length=10, blank=True, null=True)
    ano_modelo = fields.EncryptedCharField(max_length=10, blank=True, null=True)
    numero_crv = fields.EncryptedCharField(max_length=25, blank=True, null=True)

    # COL 2
    categoria = fields.EncryptedCharField(max_length=155, blank=True, null=True)
    capacidade = fields.EncryptedCharField(max_length=25, blank=True, null=True)
    potencia_cilindrada = fields.EncryptedCharField(max_length=15, blank=True, null=True)
    peso_bruto_total = fields.EncryptedCharField(max_length=25, blank=True, null=True)
    eixos = fields.EncryptedCharField(max_length=25, blank=True, null=True)
    carroceria = fields.EncryptedCharField(max_length=30, blank=True, null=True)
    cmt = fields.EncryptedCharField(max_length=25, blank=True, null=True)
    lotacao = fields.EncryptedCharField(max_length=5, blank=True, null=True)

    #COL 3
    cod_seguranca_cla = fields.EncryptedCharField(max_length=25, blank=True, null=True)
    cat = fields.EncryptedCharField(max_length=50, blank=True, null=True)
    marca_modelo_versão = fields.EncryptedCharField(max_length=75, blank=True, null=True)
    especie_tipo = fields.EncryptedCharField(max_length=75, blank=True, null=True)
    placa_anterior_uf = fields.EncryptedCharField(max_length=10, blank=True, null=True)
    chassi = fields.EncryptedCharField(max_length=75, blank=True, null=True)
    cor_predominante = fields.EncryptedCharField(max_length=35, blank=True, null=True)
    combustivel = fields.EncryptedCharField(max_length=75, blank=True, null=True)

    #COL 4
    local = fields.EncryptedCharField(max_length=18, blank=True, null=True)
    data = fields.EncryptedCharField(max_length=10, blank=True, null=True)
    motor = fields.EncryptedCharField(max_length=25, blank=True, null=True)

    def __str__(self):
        return f'{self.nome} - {self.cpf_ou_cnpj}'


class Images(models.Model):
    image = models.ImageField()


class OCRQueue(models.Model):
    image = models.ImageField(upload_to='ocrqueue/temp/')
    original_image = models.ImageField(upload_to='ocrqueue/originals/')
    image_type = fields.EncryptedCharField(max_length=2, choices=IMAGE_TYPE_CHOICES)
    number = fields.EncryptedCharField(max_length=20)


class DoneOCRQueue(models.Model):
    uuid = models.IntegerField()
    date_time = fields.EncryptedDateTimeField(default=timezone.now)
    status = fields.EncryptedCharField(max_length=2, choices=(
            ('SC', 'SUCESS'),
            ('FL', 'FAILED')
        )
    )
    number = fields.EncryptedCharField(max_length=20)

    
    def is_expired(self):
        now = timezone.now()
        elapsed_time = now - self.date_time
        return elapsed_time.total_seconds() > 900

    @classmethod
    def cleanup_expired(cls):
        """Delete expired instances"""
        expired_instances = cls.objects.filter(date_time__lt=timezone.now() - timezone.timedelta(minutes=15))
        expired_instances.delete()
