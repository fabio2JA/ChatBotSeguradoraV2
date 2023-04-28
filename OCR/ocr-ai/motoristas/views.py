from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

import json

from motoristas.handlers.image import ImageHandler
from motoristas.handlers.ocr.queue import verify_has_queue
from motoristas.handlers.queue import OCRQueueHandler
from .models import DoneOCRQueue, OCRQueue

verify_has_queue()

@require_http_methods(['GET'])
def home(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        return render(request, 'home.html')
    else:
        return HttpResponseBadRequest('only method get is acceptable')


def reconhecimento_cnh(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        return render(request, 'cnh.html')
    elif request.method == 'POST':
        image = ImageHandler.extract_image(request)
        number = request.POST.get('number')

        uuid = OCRQueueHandler.add_image_queue(image, 'CN', image, number)

        return render(request, 'cnh.html', {'uuid': uuid})
    else:
        return HttpResponseBadRequest('only method get and post are acceptable')


def reconhecimento_doc(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        return render(request, 'doc.html')
    elif request.method == 'POST':
        image = ImageHandler.extract_image(request)
        number = request.POST.get('number')

        uuid = OCRQueueHandler.add_image_queue(image, 'DC', image, number)

        return render(request, 'doc.html', {'uuid': uuid})
    else:
        return HttpResponseBadRequest('only method get and post are acceptable')


@require_http_methods(['POST'])
def verify_done_ocr(request: HttpRequest) -> HttpResponse:
    uuid = request.POST.get('uuid')
    response = None
    DoneOCRQueue.cleanup_expired()

    if uuid is not None and len(OCRQueue.objects.filter(pk=uuid)) <= 0:
        try:
            done_ocr = DoneOCRQueue.objects.get(uuid=uuid)
        except DoneOCRQueue.DoesNotExist:
            response = 'FN'
        else:
            response = done_ocr.status

    return HttpResponse(response)


@require_http_methods(['POST'])
@csrf_exempt
def reconhecimento_bot_cnh(request: HttpRequest) -> HttpResponse:
    print(request.POST)
    body = json.loads(request.body.decode())
    image_base_64 = body['image']
    image_type = body['image_type']
    number = body['number']

    image = ImageHandler.extract_base_64(image_base_64, image_type, number)

    uuid = OCRQueueHandler.add_image_queue(image, 'CN', image, number)
    
    return HttpResponse(uuid)


@require_http_methods(['POST'])
@csrf_exempt
def reconhecimento_bot_doc(request: HttpRequest) -> HttpResponse:
    body = json.loads(request.body.decode())
    image_base_64 = body['image']
    image_type = body['image_type']
    number = body['number']

    image = ImageHandler.extract_base_64(image_base_64, image_type, number)

    uuid = OCRQueueHandler.add_image_queue(image, 'DC', image, number)
    
    return HttpResponse(uuid)
