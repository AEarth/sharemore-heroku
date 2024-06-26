from django.contrib.auth.decorators import login_required

from core.filters import ItemFilter
from store.models import Category, Item, LendRequest
from userprofile.models import Userprofile


def navigation(request):
    context = {}
    item_filter = ItemFilter(request.GET, queryset=Item.objects.filter(is_deleted=False))
    # if 'items' not in context:
    #     context['items'] = Item.objects.filter(is_deleted=False)[0:6]
    context['categories'] = Category.objects.all()
    context['users'] = Userprofile.objects.all()
    context['search_form'] = item_filter.form
    return context



def base_bell(request):
    if request.user.is_authenticated:
        approved_count = LendRequest.objects.filter(requester=request.user, status='a').count()
        denied_count = LendRequest.objects.filter(requester=request.user, status='d').count()
        pending_count = LendRequest.objects.filter(giver=request.user, status='p').count()
        
        all_count = approved_count + denied_count + pending_count

        context = {
            'approved_count': approved_count,
            'denied_count': denied_count,
            'pending_count': pending_count,
            'all_count': all_count,
        }

        return context
    else:
        context = {}
    return context

# core/context_processors.py

# def navigation(request):
#     context = {}
#     # Add data only if 'items' key doesn't already exist in context
#     if 'items' not in context:
#         context['items'] = SomeModel.objects.all()  # or whatever logic you have
#     return context
