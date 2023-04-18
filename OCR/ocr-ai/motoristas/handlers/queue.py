from motoristas.handlers.ocr.queue import verify_has_queue
from motoristas.models import OCRQueue
from django.db.models import Q


class OCRQueueHandler:
    @classmethod
    def add_image_queue(cls, image, image_type: str, org_img) -> int:
        original_image = org_img

        queue = OCRQueue.objects.create(
            image=image, 
            image_type=image_type, 
            original_image=original_image
        )
        is_doing_schedule = OCRQueue.objects.filter(~Q(pk=queue.pk))
        
        if len(is_doing_schedule) == 0:
            verify_has_queue()
        
        return queue.pk
            
