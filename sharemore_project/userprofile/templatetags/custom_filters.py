from django import template

register = template.Library()

@register.filter
def filter_myitems(queryset, user):
    return queryset.filter(item__user=user)
