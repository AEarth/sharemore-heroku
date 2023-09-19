from django import template
from django.contrib.auth.decorators import login_required

from store.models import Item, LendRequest

register = template.Library()

@login_required
@register.inclusion_tag(r"templates\core\partials\account_bell.html")
def request_approved_bell(request):
    approved_requests = LendRequest.objects.filter(giver=request.user, status='a')
    request_count = approved_requests.count()

    return {'request_count' : request_count}