# Generated by Django 4.2 on 2023-04-28 18:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("motoristas", "0002_alter_cnh_acc_alter_cnh_categoria_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cnh",
            name="acc",
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name="cnh",
            name="categoria",
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name="cnh",
            name="data_emissao",
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name="cnh",
            name="data_nascimento",
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name="cnh",
            name="data_primeira_habilitacao",
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name="cnh",
            name="documento",
            field=models.CharField(blank=True, max_length=75, null=True),
        ),
        migrations.AlterField(
            model_name="cnh",
            name="local",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="cnh",
            name="nome",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="cnh",
            name="numero_cel",
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name="cnh",
            name="numero_registro",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name="cnh",
            name="permissao",
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name="cnh",
            name="validade",
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name="doccarro",
            name="ano_fabricacao",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="doccarro",
            name="ano_modelo",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="doccarro",
            name="capacidade",
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name="doccarro",
            name="carroceria",
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name="doccarro",
            name="cat",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="doccarro",
            name="categoria",
            field=models.CharField(blank=True, max_length=155, null=True),
        ),
        migrations.AlterField(
            model_name="doccarro",
            name="chassi",
            field=models.CharField(blank=True, max_length=75, null=True),
        ),
        migrations.AlterField(
            model_name="doccarro",
            name="cmt",
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name="doccarro",
            name="cod_renavam",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name="doccarro",
            name="cod_seguranca_cla",
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name="doccarro",
            name="combustivel",
            field=models.CharField(blank=True, max_length=75, null=True),
        ),
        migrations.AlterField(
            model_name="doccarro",
            name="cor_predominante",
            field=models.CharField(blank=True, max_length=35, null=True),
        ),
        migrations.AlterField(
            model_name="doccarro",
            name="cpf_ou_cnpj",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name="doccarro",
            name="data",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="doccarro",
            name="eixos",
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name="doccarro",
            name="especie_tipo",
            field=models.CharField(blank=True, max_length=75, null=True),
        ),
        migrations.AlterField(
            model_name="doccarro",
            name="exercicio",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="doccarro",
            name="local",
            field=models.CharField(blank=True, max_length=18, null=True),
        ),
        migrations.AlterField(
            model_name="doccarro",
            name="lotacao",
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name="doccarro",
            name="marca_modelo_versão",
            field=models.CharField(blank=True, max_length=75, null=True),
        ),
        migrations.AlterField(
            model_name="doccarro",
            name="motor",
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name="doccarro",
            name="nome",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="doccarro",
            name="numero_cel",
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name="doccarro",
            name="numero_crv",
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name="doccarro",
            name="peso_bruto_total",
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name="doccarro",
            name="placa",
            field=models.CharField(blank=True, max_length=7, null=True),
        ),
        migrations.AlterField(
            model_name="doccarro",
            name="placa_anterior_uf",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="doccarro",
            name="potencia_cilindrada",
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name="doneocrqueue",
            name="date_time",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="doneocrqueue",
            name="number",
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name="doneocrqueue",
            name="status",
            field=models.CharField(
                choices=[("SC", "SUCESS"), ("FL", "FAILED")], max_length=2
            ),
        ),
        migrations.AlterField(
            model_name="ocrqueue",
            name="image_type",
            field=models.CharField(
                choices=[("CN", "CNH"), ("DC", "CAR DOC")], max_length=2
            ),
        ),
        migrations.AlterField(
            model_name="ocrqueue",
            name="number",
            field=models.CharField(max_length=20),
        ),
    ]