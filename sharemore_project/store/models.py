from django.db import models
from django.db.models import Sum

from django.contrib.auth.models import User
from django.core.files import File

from io import BytesIO
from PIL import Image


class LendRequest(models.Model):
    requester = models.ForeignKey(User, related_name='requester', on_delete=models.SET_NULL, null=True)
    giver = models.ForeignKey(User, related_name='giver', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    pickup_date = models.DateField(help_text='Anticipated pickup day')
    return_date = models.DateField(help_text='Anticipated return day')
    REQUEST_STATUS = (
        ('p', 'Pending'),
        ('a', 'Approved'),
        ('d', 'Denied'),
    )
    status = models.CharField(max_length=1, choices=REQUEST_STATUS, default='p')
    
    def item_count(self):
    #     return self.request_items.item.count()
        return self.request_items.aggregate(sum=Sum('quantity'))['sum'] or 0
    
    def __str__(self):
        if self.status == 'a':
            return f"{self.giver} approved your request"
        
        elif self.status == 'd':
            return f"{self.giver} denied your request"
        
        elif self.status == 'p':
            return f"{self.requester} requested {self.item_count()} item(s)"
     
    # Requested {self.item_count()}
class RequestItems(models.Model):
    verbose_name = "Request Item"
    lend_request = models.ForeignKey('LendRequest', related_name='request_items', on_delete=models.CASCADE)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    value = models.IntegerField()
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.item} - {self.quantity}" 

            
class Category(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    
    class Meta:
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.title
    
    
class Item(models.Model):
    user = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    description = models.TextField(blank=True)
    value = models.IntegerField()
    image = models.ImageField(upload_to='uploads/item_images/', blank=True, null=True)
    image_med = models.ImageField(upload_to='uploads/item_images_med/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/item_thumbnails/', blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    is_deleted = models.BooleanField(default=False)
    
    class Meta:
        ordering = ('-created_date',)
    
    def __str__(self):
        return self.title
    
    def get_display_value(self):
        price = self.value / 100 
        return f"{price:.2f}"
    
    def get_title(self):
        if len(self.title)> 20:
            return self.title[:20] + '...'
        return self.title
    
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
            


# class LendPeriod(models.Model):
#     lend_request = models.OneToOneField('LendAsk', on_delete=models.CASCADE)
#     start_date = models.DateField(help_text='Start date of the lend')
#     end_date = models.DateField(help_text='End date of the lend')
    
#     # def __str__(self):
#     #     return f"{self.loan_request.tool} loaned from {self.start_date} to {self.end_date}"
         