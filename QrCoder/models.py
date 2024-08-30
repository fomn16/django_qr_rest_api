from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import default_storage

class QrCode(models.Model):
    id = models.AutoField(primary_key=True)
    encodedInfo = models.CharField(max_length=100)
    image = models.ImageField(upload_to='QrCodeImageStorage', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def delete(self, *args, **kwargs):
        if self.image:
            default_storage.delete(self.image.path)
        super().delete(*args, **kwargs)
