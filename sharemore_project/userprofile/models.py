from django.db import models

from django.contrib.auth.models import User

from django.core.files import File
from io import BytesIO
from PIL import Image


# Create your models here.
class Userprofile(models.Model):
    user = models.OneToOneField(User, related_name='userprofile', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/item_images/', verbose_name='Profile Pic', blank=True, null=True)
    image_med = models.ImageField(upload_to='uploads/item_images_med/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/item_thumbnails/', blank=True, null=True)
    
    summary = models.CharField(max_length=200, verbose_name='Catch Phrase', blank=True, null=True)
    full_text = models.TextField(verbose_name='Bio', blank=True, null=True)
    social_url = models.URLField(verbose_name='Social URL', blank=True, null=True)
    
    def make_thumbnail(self, image, size=(75,75)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)
        
        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)
        name = image.name.replace('uploads/item_images/', '')
        thumbnail = File(thumb_io, name=name)
        
        return thumbnail

    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                
                return self.thumbnail.url

    def get_image_med(self):
        if self.image_med:
            return self.image_med.url
        else:
            if self.image:
                self.image_med = self.make_thumbnail(self.image, size=(300,300))
                self.save()
                
                return self.image_med.url
    
    
    def __str__(self):
        return self.user.username