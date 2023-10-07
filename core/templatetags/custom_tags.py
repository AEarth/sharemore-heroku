from django import template
from django.contrib.auth.decorators import login_required

from store.models import Item, LendRequest

register = template.Library()

@login_required
# @register.inclusion_tag(r"templates\core\partials\request_account_bell.html")
def request_account_bell(request):
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


    #return {'request_count' : request_count}
    return context