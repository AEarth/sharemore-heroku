from django.contrib import admin

# Register your models here.

from .models import Category, Item, LendRequest, RequestItems

admin.site.register(Category)

admin.site.register(RequestItems)


class RequestItemsInline(admin.TabularInline):
    model = RequestItems
    extra = 0  # Number of empty forms to display

@admin.register(LendRequest)
class LendRequestAdmin(admin.ModelAdmin):
    inlines = (RequestItemsInline,)
    list_display = ('requester', 'giver', 'workflow_state', 'created_at', 'pickup_date', 'return_date')
    
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'user')