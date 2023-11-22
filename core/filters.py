import django_filters
from django import forms
from django.db.models import Q

from store.models import Item


class ItemFilter(django_filters.FilterSet):
    text_search = django_filters.CharFilter(method='custom_textsearch', label='Title or Description', widget=forms.TextInput(attrs={'placeholder': 'Search', 'class': 'input input-sm input-bordered join-item input-primary w-full'}))
    price_greater = django_filters.NumberFilter(field_name='value', lookup_expr='gte', label='min', widget=forms.TextInput(attrs={'placeholder': 'min','class': 'w-1/3 font-normal text-center'}))
    price_less = django_filters.NumberFilter(field_name='value', lookup_expr='lte', label='max', widget=forms.TextInput(attrs={'placeholder': 'max','class': 'w-1/3 font-normal text-center'}))
      
    class Meta:
        model = Item
        fields = {
            'category': ['exact']
        }
        
    def custom_textsearch(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value) |
            Q(description__icontains=value)
        )