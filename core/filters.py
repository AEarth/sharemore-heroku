import django_filters
from django import forms
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.db.models import Q
from threadlocals.threadlocals import get_current_request

from store.models import Item


class ItemFilter(django_filters.FilterSet):
    text_search = django_filters.CharFilter(method='custom_textsearch', label='Title or Description', widget=forms.TextInput(attrs={'placeholder': 'Search', 'class': 'input input-sm input-bordered join-item input-primary w-full'}))
    price_greater = django_filters.NumberFilter(field_name='value', lookup_expr='gte', label='min', widget=forms.TextInput(attrs={'placeholder': 'min','class': 'w-1/3 font-normal text-center'}))
    price_less = django_filters.NumberFilter(field_name='value', lookup_expr='lte', label='max', widget=forms.TextInput(attrs={'placeholder': 'max','class': 'w-1/3 font-normal text-center'}))
    
    distance = django_filters.NumberFilter(method="distance_filter", label='miles', widget=forms.TextInput(attrs={'placeholder': 'miles','class': 'w-1/3 font-normal text-center'}))
    
    
    
    class Meta:
        model = Item
        fields = {
            'category': ['exact']
        }
        
    def distance_filter(self, queryset, name, miles):
        user = get_current_request().user
        if not user.userprofile.lat:
            print("user has no location stored")
            return queryset  # or handle this case differently

        user_location = Point(float(user.userprofile.lon), float(user.userprofile.lat), srid=4326)

        # Assuming 'point' is a PointField on your model
        return queryset.annotate(
            distance=Distance('point', user_location)
        ).filter(distance__lte=D(mi=miles))                                                                                     
        
        
    def custom_textsearch(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value) |
            Q(description__icontains=value)
        )
        
    # def distance_filter(self, queryset, name, miles):
    #     user_location = (self.user.userprofile.lat, self.user.userprofile.lon)
    #     item_location = (self.item.lat, self.item.lon)
    #     return queryset.filter(
    #         dist(user_location, item_location).miles <= miles
    #     )