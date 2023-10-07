from django.db import models
from django.db.models import Sum

from django.contrib.auth.models import User
from django.core.files import File

from io import BytesIO
from PIL import Image

from datetime import datetime
from django.db.models.signals import post_save

from django.contrib.auth import get_user_model
from django_fsm import FSMField, transition

from django.shortcuts import render, get_object_or_404, redirect

# from sharemore.middleware import CurrentUserMiddleware
# import threading

from threadlocals.threadlocals import get_current_request


# request_cfg = threading.local()
# #user = getattr(request_cfg, 'user', None)

# def get_user_model(request):
#     user = CurrentUserMiddleware.get_user(request)
#     return user

# get_user_model(request_cfg)

class WorkflowState(object):
    # constants to represent the states of the lendrequest model workflow
    PENDING = 'pending'
    DENIED = 'denied'
    EXPIRED = 'expired'
    APPROVED = 'approved'
    RECEIVED = 'received'
    OVERDUE = 'overdue'
    RETURNED = 'returned'

    CHOICES = (
        (PENDING, PENDING.title()),
        (DENIED, DENIED.title()),
        (EXPIRED, EXPIRED.title()),
        (APPROVED, APPROVED.title()),
        (RECEIVED, RECEIVED.title()),
        (OVERDUE, OVERDUE.title()),
        (RETURNED, RETURNED.title()),
    )

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
    
    workflow_state = FSMField(default=WorkflowState.PENDING, verbose_name="request status", choices=WorkflowState.CHOICES, protected=False)
    
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
    
    # # some copy/paste on getting the user in models.py
        # if kwargs.has_key('request') and self.user is None:
        #         request = kwargs.pop('request')
        #         self.user= request.user
        # super(StockTickerSymbol, self).save(**kwargs)
        
    

    ########################################################
    # Transition Conditions
    # These must be defined prior to the actual transitions
    # to be refrenced.
    
    def stay_pending(self):
        if self.workflow_state in (WorkflowState.PENDING):
            return True
        return False
    
    def can_approve_deny(self):
        user = get_current_request().user
        if self.workflow_state in (WorkflowState.PENDING, WorkflowState.DENIED) and user.username == self.giver.username:
            return True
        return False

    def can_receive(self):
        user = get_current_request().user
        if self.workflow_state in (WorkflowState.APPROVED) and user.username == self.requester.username:
            return True
        return False
    
    def is_expired(self):
        return self.state == WorkflowState.EXPIRED
    
    def is_overdue(self):
        return self.state == WorkflowState.OVERDUE

    def can_accept_return(self):
        user = get_current_request().user
        if self.workflow_state in (WorkflowState.RECEIVED) and user.username == self.giver.username:
            return True
        return False
    
    
    def check_expired(self):
        ## check if request is past return_date if it is change state to expired
        expired = self.return_date < datetime.now().date()
        
        # Expired Pages should transition to the expired state
        if not expired and not self.is_expired and self.workflow_state in (WorkflowState.PENDING, WorkflowState.APPROVED):
            self.expire()  # Calling the expire transition
            self.save()
        return expired
    
    
    def check_overdue(self):
        ## check if request is past return_date if it is change state to expired
        overdue = self.return_date < datetime.now().date()
        
        if overdue and not self.is_overdue and self.workflow_state == WorkflowState.RECEIVED:
            self.overdue()  # Calling the overdue transition
            self.save()
        return overdue
    
    ########################################################
    # Workflow (state) Transitions
    
    @transition(field=workflow_state, source=[WorkflowState.PENDING],
    target=WorkflowState.PENDING,
    conditions=[stay_pending]
    )
    def pending(self):
        ##put any actions needed here
        pass
    
    @transition(field=workflow_state, source=[WorkflowState.PENDING],
        target=WorkflowState.APPROVED,
        conditions=[can_approve_deny]
        )
    def approved(self):
        ##put any actions needed here
        pass
    
    @transition(field=workflow_state, source=[WorkflowState.PENDING],
        target=WorkflowState.DENIED,
        conditions=[can_approve_deny]
        )
    def denied(self):
        ##put any actions needed here
        pass
     
    @transition(field=workflow_state, source=[WorkflowState.PENDING, WorkflowState.APPROVED,WorkflowState.DENIED],
        target=WorkflowState.EXPIRED,
        conditions=[check_expired]
        )
    def expire(self):
        return self.WorkflowState.EXPIRED
    
    @transition(field=workflow_state, source=[WorkflowState.APPROVED],
        target=WorkflowState.RECEIVED,
        conditions=[can_receive]
        )
    def received(self):
        ##put any actions needed here
        pass
    
    @transition(field=workflow_state, source=[WorkflowState.RECEIVED],
        target=WorkflowState.OVERDUE,
        conditions=[check_overdue]
        )
    def overdue(self):
        ##put any actions needed here
        pass
    
    @transition(field=workflow_state, source=[WorkflowState.RECEIVED],
        target=WorkflowState.RETURNED,
        conditions=[can_accept_return]
        )
    def overdue(self):
        ##put any actions needed here
        pass
    
    class Meta:
        permissions = [
            ("can_publish_post", "Can publish post"),
            ("can_remove_post", "Can remove post"),
        ]

    
########################################################
# Other Models
      
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
    
    def make_images(self):
        self.thumbnail = self.make_thumbnail(self.image)
        print(f"Updated thumbnail {self.thumbnail}")
        self.image_med = self.make_thumbnail(self.image, size=(300,300))
        print(f"Updated medium img {self.image_med}")
        

    def save(self, *args, **kwargs):         
        #check if image update
        if self.pk:
            orig = Item.objects.get(pk=self.pk)
            #check if image file changed
            if orig.image != self.image:
                self.make_images()
                super().save(*args, **kwargs)
            else:
                super().save(*args, **kwargs)
        #first first form completion with image uploaded create thumbs 
        if self.pk is None and self.image:
            self.make_images()
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)

    
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
        img = img.convert('RGB')
        img.thumbnail(size)
        
        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)
        name = image.name.replace('uploads/item_images/', '')
        thumbnail = File(thumb_io, name=name)
        
        return thumbnail
    
    # def get_thumbnail(self):
    #     if self.thumbnail:
    #         return self.thumbnail.url
    #     elif self.image:
    #         self.thumbnail = self.make_thumbnail(self.image)
    #         self.save()
            
    #         return self.thumbnail.url
    #     else:
    #         return False
  
  
    # def get_image_med(self):
    #     if self.image_med:
    #         print("found image_med")
    #         return self.image_med.url
    #     elif self.image:
    #             self.image_med = self.make_thumbnail(self.image, size=(300,300))
    #             self.save()
    #             return self.image_med.url
    #     return "/static/default_img/item.png"


# class LendPeriod(models.Model):
#     lend_request = models.OneToOneField('LendAsk', on_delete=models.CASCADE)
#     start_date = models.DateField(help_text='Start date of the lend')
#     end_date = models.DateField(help_text='End date of the lend')
    
#     # def __str__(self):
#     #     return f"{self.loan_request.tool} loaned from {self.start_date} to {self.end_date}"
         