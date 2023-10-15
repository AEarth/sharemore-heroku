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
    
    
    def get_all_bell_count(request):
        approve_count = request.user.LendRequest.objects.filter(requester=request.user, status='a').count()
        denied_count = request.user.LendRequest.objects.filter(requester=request.user, status='d').count()
        pending_count = request.user.adeleteLendRequest.objects.filter(giver=request.user, status='p').count()
        
        all_count = approve_count + denied_count + pending_count


    def save(self, *args, **kwargs):
        #check if update
        if self.pk:
            orig = Userprofile.objects.get(pk=self.pk)
            #check if image file changed
            if orig.image != self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                print(f"Updated thumbnail {self.thumbnail}")
                self.image_med = self.make_thumbnail(self.image, size=(300,300))
                print(f"Updated medium img {self.image_med}")
                super().save(*args, **kwargs)
            else:
                super().save(*args, **kwargs)
        #if create
        if self.pk is None and self.image:
            self.thumbnail = self.make_thumbnail(self.image)
            print(f"created thumbnail {self.thumbnail}")
            self.image_med = self.make_thumbnail(self.image, size=(300,300))
            print(f"created medium img {self.image_med}")
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)

        
    
    def make_thumbnail(self, image, size=(75,75)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)
        
        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)
        name = image.name.replace('uploads/item_images/', '')
        thumbnail = File(thumb_io, name=name)
        
        return thumbnail

    
    def __str__(self):
        return self.user.username