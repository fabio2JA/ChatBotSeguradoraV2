from django.http import HttpRequest
from django.core.files.base import ContentFile
from datetime import datetime

from PIL import Image
import tempfile
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile

import base64
from io import BytesIO
from pdf2image import convert_from_bytes

from motoristas.models import Images


class ImageHandler:
    @classmethod
    def handle_extract_infos_request(cls, form_data: dict) -> dict:
        new_form_data = {}
        for key, value in form_data:
            if key != 'csrfmiddlewaretoken' and value != '':
                new_value = value
                try:
                    new_value = datetime.strptime(new_value, '%d/%m/%Y').date()
                except Exception:
                    pass
                new_form_data[key] = value
        for key, value in new_form_data.items():
            if key in ['data_nascimento', 'validade', 'data_primeira_habilitacao', 'data_emissao']:
                date_obj = datetime.strptime(value, '%d/%m/%Y').date()
                new_form_data[key] = date_obj
        return new_form_data

    
    @classmethod
    def extract_image(cls, request: HttpRequest):
        image = request.FILES.get('image')

        image = cls.upload_file_to_image(image)

        for img in Images.objects.all():
            img.image.delete()
            img.delete()

        image = Images.objects.create(image=image)
        image.save()
        return image.image
    
    @classmethod
    def extract_base_64(cls, image: str, type: str, number: str):
        if type == 'jpg' or type == 'jpeg' or type == 'png':
            image_bytes = base64.b64decode(image)
            image_file = BytesIO(image_bytes)
            image = Image.open(image_file)

            image_name = f'{number}.{type}'  # Replace with desired file name
            image_field = SimpleUploadedFile(image_name, image_file.getvalue())
            image = Images.objects.create(image=image_field)
            image.save()
            return image.image
        elif type == 'pdf':
            pdf_bytes = base64.b64decode(image)
            with tempfile.NamedTemporaryFile(delete=False) as f:
                f.write(pdf_bytes)
            pdf_file = File(open(f.name, 'rb'))
            pdf_name = f'{number}.{type}'
            pdf_field = SimpleUploadedFile(pdf_name, pdf_file.read())
            pdf = Images.objects.create(image=pdf_field)
            pdf.save()
            return pdf.image


    
    @classmethod
    def upload_file_to_image(cls, img):
        image = img
        if img.content_type == 'application/pdf':
            file_bytes = img.read()

            image_list = convert_from_bytes(file_bytes)

            image_file_list = []
            for i, image in enumerate(image_list):
                image_file = BytesIO()
                image.save(image_file, 'JPEG')
                image_file.name = f'{img.name}_page_{i+1}.jpeg'
                image_file_list.append(image_file)

            image_file = image_file_list[0]

            image_data = image_file.getvalue()
            image_name = image_file.name
            image_content = ContentFile(image_data)
            image_content.name = image_name
            image = image_content
        return image
    