import cv2
from django.core.files.base import ContentFile
from django.core.files.images import ImageFile
import numpy as np
from motoristas.models import Images

class CNHHandler:
    @classmethod
    def clean_cnh(cls, image):
        # GET RECTANGLES
        rectangles = []
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lower_green = np.array([30, 50, 50])
        upper_green = np.array([70, 255, 255])
        mask = cv2.inRange(hsv, lower_green, upper_green)
        coords = np.column_stack(np.where(mask > 0))
        x_min, y_min = np.min(coords, axis=0)
        x_max, y_max = np.max(coords, axis=0)
        rectangles.append((y_min, x_min))
        rectangles.append((y_max, x_max))

        # CROPP IMAGE
        img = image[x_min:x_max, y_min:y_max]

        # SAVE IMAGE
        cv2.imwrite('temp.jpg', img)
        with open('temp.jpg', 'rb') as f:
            image_data = f.read()

        # Create a ContentFile object from the binary data
        content_file = ContentFile(image_data)

        # Create a new Image object and set its FileField to the ContentFile object
        my_model = Images()
        my_model.image.save('temp.jpg', ImageFile(content_file))
        # Create a ContentFile object from the binary data
        content_file = ContentFile(image_data)
        my_model.save()
        image = my_model.image

        return image.path
    