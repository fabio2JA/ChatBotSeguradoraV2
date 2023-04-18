from django.http import HttpRequest
from django.core.files.base import ContentFile
from datetime import datetime

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
    def upload_file_to_image(cls, img):
        image = img
        if img.content_type == 'application/pdf':
            file_bytes = img.read()

            # Convert PDF to list of PIL.Image objects using pdf2image
            image_list = convert_from_bytes(file_bytes)

            print(image_list)

            # Save each image to a BytesIO object
            image_file_list = []
            for i, image in enumerate(image_list):
                image_file = BytesIO()
                image.save(image_file, 'JPEG')
                image_file.name = f'{img.name}_page_{i+1}.jpeg'
                image_file_list.append(image_file)

            image_file = image_file_list[0]

            # Create a new InMemoryUploadedFile object from the first image file
            image_data = image_file.getvalue()
            image_name = image_file.name
            image_content = ContentFile(image_data)
            image_content.name = image_name
            image = image_content
        return image
    