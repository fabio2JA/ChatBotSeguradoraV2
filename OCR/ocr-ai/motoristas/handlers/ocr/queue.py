import time
import cv2
import threading

import requests
import json

from django.utils import timezone

from motoristas.handlers.cnh import CNHHandler
from motoristas.handlers.image import ImageHandler
# from motoristas.handlers.ocr.ocr import OCRRecognitor
from motoristas.models import CNH, DOCCarro, DoneOCRQueue, OCRQueue


def verify_has_queue():
    queues = OCRQueue.objects.all()
    if len(queues) > 0:
        queue_one = queues[0]
        thread = threading.Thread(
            target=do_queue, 
            args=(queue_one,)
        )
        thread.start()

def do_queue(queue: OCRQueue):
    # DELETAR
    time.sleep(15)

    done_ocr = DoneOCRQueue.objects.create(
        uuid=queue.pk, 
        status='FL', 
        number=queue.number
    )

    #  DELETAR
    queue.image.delete()
    queue.original_image.delete()
    queue.delete()

    done_ocr.date_time = timezone.now()
    done_ocr.save()

    send_status_ocr(done_ocr.status, done_ocr.number)

    verify_has_queue()
    
    # try:
    #     extracted_infos = do_ocr(queue)
    #     save_ocr_on_db(extracted_infos, queue.image_type, done_ocr)
    # except Exception as e:
    #     pass
    # finally:
    #     queue.image.delete()
    #     queue.original_image.delete()
    #     queue.delete()

    #     done_ocr.date_time = timezone.now()
    #     done_ocr.save()

    #     verify_has_queue()


def do_ocr(queue: OCRQueue) -> dict:
    image_to_extract = queue.image.path
    fields_to_extract_regex = []
    fields_to_extract_extration = {}

    if queue.image_type == 'CN':
        image_to_extract = CNHHandler.clean_cnh(cv2.imread(queue.image.path))
        fields_to_extract_regex = [
            'nome', 'datanascimento', 'validade', 'nregistro', '1habilitacao', 'observacoes',
            'dataemissao', 'cathab', 'cpf', 'datanascimento', 'permissao', 'acc',
            'docidentidadeorgemissoruf', 'filiacao', 'local'
        ]
        fields_to_extract_extration = {
            'nome': 'nome', 'data_nascimento': 'datanascimento', 'validade': 'validade',
            'numero_registro': 'nregistro', 'data_primeira_habilitacao': '1habilitacao',
            'data_emissao': 'dataemissao', 'categoria': 'cathab', 'cpf': 'cpf',
            'permissao': 'permissao', 'acc': 'acc',
            'documento': 'docidentidadeorgemissoruf', 'local': 'local'
        }
    elif queue.image_type == 'DC':
        fields_to_extract_regex = [
            'codigorenavam', 'placa', 'exercicio', 'chassi', 'cmt', 'eixos', 'lotacao',
            'categoria', 'capacidade', 'potnciacilindrada', 'pesobrutototal',  'motor',
            'carroceria', 'cat', 'anofabricacao', 'anomodelo',
            'numerodocrv', 'cpfcnpj', 'local', 'data', 'combustvel', 'corpredominante', 
            'marcamodeloversao', 'espcietipo', 'cdigodesegurancadocla', 'placaanterioruf',
            'nome'
        ]
        fields_to_extract_extration = {
            'cod_renavam': 'codigorenavam', 'placa': 'placa', 
            'exercicio': 'exercicio', 'chassi': 'chassi', 'cmt': 'cmt', 'eixos': 'eixos',
            'lotacao': 'lotacao', 'categoria': 'categoria', 'capacidade': 'capacidade', 
            'potencia_cilindrada': 'potnciacilindrada', 'peso_bruto_total': 'pesobrutototal', 
            'motor': 'motor', 'carroceria': 'carroceria', 'cat': 'cat', 'ano_fabricacao': 'anofabricacao', 
            'ano_modelo': 'anomodelo', 'numero_crv': 'numerodocrv', 'cpf_ou_cnpj': 'cpfcnpj', 
            'local': 'local', 'data': 'data', 'combustivel': 'combustvel', 
            'cor_predominante': 'corpredominante', 'marca_modelo_versão': 'marcamodeloversao', 
            'especie_tipo': 'espcietipo', 'cod_seguranca_cla': 'cdigodesegurancadocla', 
            'placa_anterior_uf': 'placaanterioruf', 'nome': 'nome'
        }

    extracted_info = {'': ''}
    try:
        # ocr = OCRRecognitor(
        #     image_to_extract,
        #     fields_to_extract_regex,
        #     []
        # )
        # extracted_info = ocr.recognize(fields_to_extract_extration)
        print('o')
    except Exception:
        raise ValueError('ERRO AO RECONHECER A IMAGEM')
    else:
        # extracted_info['image'] = queue.original_image
        return extracted_info
    
    
def save_ocr_on_db(extracted_info: dict, image_type: str, done_ocr: DoneOCRQueue):
    extracted_info = ImageHandler.handle_extract_infos_request(extracted_info.items())
    if image_type == 'CN':
        cnh = CNH.objects.create(**extracted_info)
        cnh.save()
    elif image_type == 'DC':
        doc = DOCCarro.objects.create(**extracted_info)
        doc.save()
    done_ocr.status = 'SC'
    done_ocr.save()


def send_status_ocr(status: str, number: str):
    url = 'http://localhost:3000/status/'

    data = {
        'status': status,
        'number': number
    }

    headers = {
        'Content-Type': 'application/json',
        'mode': 'cors'
    }

    try:
        requests.post(url, data=json.dumps(data), headers=headers, timeout=10)
    except Exception:
        pass
