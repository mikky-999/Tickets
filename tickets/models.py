from django.db import models
from PIL import Image, ImageDraw
import qrcode
from io import BytesIO
from django.core.files import File
from django.contrib.auth.models import User
import uuid


class Event(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateTimeField()

    def __str__(self):
        return self.name

class Ticket(models.Model):
    code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    is_used = models.BooleanField(default=False)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True)

    def __str__(self):
        return f"{self.event.name} - {self.owner.username}"

    
    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)

        if not self.qr_code:
            qrcode_img = qrcode.make(self.code)
            canvas = Image.new('RGB', (qrcode_img.pixel_size, qrcode_img.pixel_size), 'white')
            draw = ImageDraw.Draw(canvas)
            canvas.paste(qrcode_img)
            buffer = BytesIO()
            canvas.save(buffer, 'PNG')
            self.qr_code.save(f'qr_code-{self.code}.png', File(buffer), save=False)
            canvas.close()
            super().save(*args, **kwargs)

# Create your models here.