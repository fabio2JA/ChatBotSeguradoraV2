from django.db import models
from django.utils import timezone

from motoristas.constants import IMAGE_TYPE_CHOICES

class CNH(models.Model):
    image = models.ImageField()
    cpf = models.CharField(max_length=14, null=False, blank=False, primary_key=True)
    nome = models.CharField(max_length=255, blank=True, null=True)
    documento = models.CharField(max_length=75, blank=True, null=True)
    data_nascimento = models.CharField(max_length=25, blank=True, null=True)
    validade = models.CharField(max_length=25, blank=True, null=True)
    numero_registro = models.CharField(max_length=20, blank=True, null=True)
    data_primeira_habilitacao = models.CharField(max_length=25, blank=True, null=True)
    permissao = models.CharField(max_length=15, blank=True, null=True)
    acc = models.CharField(max_length=15, blank=True, null=True)
    categoria = models.CharField(max_length=3, blank=True, null=True)
    data_emissao = models.CharField(max_length=25, blank=True, null=True)
    local = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'{self.nome} - {self.cpf}'

class DOCCarro(models.Model):
    image = models.ImageField()
    cpf_ou_cnpj = models.CharField(max_length=20, blank=True, null=True)
    nome = models.CharField(max_length=255, blank=True, null=True)

    # COL 1
    cod_renavam = models.CharField(max_length=20, blank=True, null=True)
    placa = models.CharField(max_length=7, blank=True, null=True)
    exercicio = models.CharField(max_length=10, blank=True, null=True)
    ano_fabricacao = models.CharField(max_length=10, blank=True, null=True)
    ano_modelo = models.CharField(max_length=10, blank=True, null=True)
    numero_crv = models.CharField(max_length=25, blank=True, null=True)

    # COL 2
    categoria = models.CharField(max_length=155, blank=True, null=True)
    capacidade = models.CharField(max_length=25, blank=True, null=True)
    potencia_cilindrada = models.CharField(max_length=15, blank=True, null=True)
    peso_bruto_total = models.CharField(max_length=25, blank=True, null=True)
    eixos = models.CharField(max_length=25, blank=True, null=True)
    carroceria = models.CharField(max_length=30, blank=True, null=True)
    cmt = models.CharField(max_length=25, blank=True, null=True)
    lotacao = models.CharField(max_length=5, blank=True, null=True)

    #COL 3
    cod_seguranca_cla = models.CharField(max_length=25, blank=True, null=True)
    cat = models.CharField(max_length=50, blank=True, null=True)
    marca_modelo_versão = models.CharField(max_length=75, blank=True, null=True)
    especie_tipo = models.CharField(max_length=75, blank=True, null=True)
    placa_anterior_uf = models.CharField(max_length=10, blank=True, null=True)
    chassi = models.CharField(max_length=75, blank=True, null=True)
    cor_predominante = models.CharField(max_length=35, blank=True, null=True)
    combustivel = models.CharField(max_length=75, blank=True, null=True)

    #COL 4
    local = models.CharField(max_length=18, blank=True, null=True)
    data = models.CharField(max_length=10, blank=True, null=True)
    motor = models.CharField(max_length=25, blank=True, null=True)

    def __str__(self):
        return f'{self.nome} - {self.cpf_ou_cnpj}'


class Images(models.Model):
    image = models.ImageField()


class OCRQueue(models.Model):
    image = models.ImageField(upload_to='ocrqueue/temp/')
    original_image = models.ImageField(upload_to='ocrqueue/originals/')
    image_type = models.CharField(max_length=2, choices=IMAGE_TYPE_CHOICES)
    number = models.CharField(max_length=20)


class DoneOCRQueue(models.Model):
    uuid = models.IntegerField(primary_key=True)
    date_time = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=2, choices=(
            ('SC', 'SUCESS'),
            ('FL', 'FAILED')
        )
    )
    number = models.CharField(max_length=20)

    
    def is_expired(self):
        now = timezone.now()
        elapsed_time = now - self.date_time
        return elapsed_time.total_seconds() > 900

    @classmethod
    def cleanup_expired(cls):
        """Delete expired instances"""
        expired_instances = cls.objects.filter(date_time__lt=timezone.now() - timezone.timedelta(minutes=15))
        expired_instances.delete()
