import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.core.serializers import serialize
from django.db.models import Q
from django.http import HttpResponseNotFound, QueryDict
from django.shortcuts import get_object_or_404, redirect, render

from core.context_processors import navigation
from core.filters import ItemFilter
#from sharemore.settings import MEDIA_URL
from store.cart import Cart
from store.models import Item


def frontpage(request):
    context = {}
    
    item_filter = ItemFilter(request.GET, queryset=Item.objects.filter(is_deleted=False))
    context['items'] = item_filter.qs
    context['search_form'] = item_filter.form
    
    # Check if the view preference is already in the session
    current_view = request.session.get('view_preference', 'grid')  # Default to 'grid'
    context['current_view'] = current_view

    # If the view parameter is in the request, update the session
    if 'view' in request.GET:
        current_view = request.GET['view']
        request.session['view_preference'] = current_view  # Save in session
    
    if current_view == "map":
        geojson = serialize('geojson', item_filter.qs, geometry_field='point', fields=('title', 'description', 'point', 'category', 'value', 'image', 'image_med', 'thumbnail', 'image_med.url', 'id', 'item.user.userprofile.thumbnail'))
        print(geojson)
        context['points'] = json.loads(geojson)
        #context['media_url'] = MEDIA_URL
        
    print("Current view pref:", current_view)

    # if request.GET.get('view'):
    #     context['current_view'] = request.GET.get('view') 

    if 'HX-Request' in request.headers:
        if request.GET.get("view") == "grid":
            template = "store/item_grid.html"
            return render(request, template, context)

        if request.GET.get("view") == "list":
            template = "store/item_list.html"
            return render(request, template, context)
        
        if request.GET.get("view") == "map":
            template = "store/item_map.html"
            print(json.loads(geojson))
            return render(request, template, context)

    return render(request, "core/frontpage.html", context)


def base(request):
    # search form in context_processor
    # bell stuff is now in context_processor
    context = {}
    return render(request, "core/base.html", context)


    # Paginate the results, assuming you want 6 items per page
    # paginator = Paginator(context["items"], 6)
    # page_number = request.GET.get("page")
    # context["items"] = paginator.get_page(page_number)



# def frontpage(request):
#     context = {}

#     # Search bar
#     search = request.GET.get('search')
#     if search:
#         context["items"] = Item.objects.filter(
#             Q(title__icontains=search) |
#             Q(description__icontains=search)
#         )[:6]
#     else:
#         context["items"] = Item.objects.filter(is_deleted=False)[:6]

#     if request.method == "POST":
#         print(request.POST)
#         if "listview" in request.POST:
#             print(request.POST)
#             return render(request, "store/item_list.html", context)
#         elif "gridview" in request.POST:
#             print(request.POST)
#             return render(request, "store/item_grid.html", context)

#     return render(request, "core/frontpage.html", context)


# if request.htmx:
#     print(request.htmx.current_url)
#     return render(request, 'store/item_list.html', context)
#     print(request.GET.get('list-view'))


def gridview(request):
    context = {}
    context["items"] = Item.objects.filter(is_deleted=False)[0:6]

    if request.htmx:
        print(request.htmx.current_url)
        return render(request, "store/item_grid.html", context)
    else:
        return HttpResponseNotFound()


def listview(request):
    context = {}
    context["items"] = Item.objects.filter(is_deleted=False)[0:6]

    if request.htmx:
        print(request.htmx.current_url)
        return render(request, "store/item_list.html", context)
    else:
        return HttpResponseNotFound()


def about(request):
    context = {}

    return render(request, "core/about.html", context)


def styles(request):
    context = {}
    return render(request, "core/styles.html", context)


# from userprofile.models import Userprofile
# from django.views.generic import TemplateView

# class ContextMixin:
#     def get_context(self):
#         items = Item.objects.all()[:6]
#         categories = Category.objects.all()
#         users = Userprofile.objects.all()
#         return {'items': items, 'categories': categories, 'users': users}

# class BaseView(ContextMixin, TemplateView):
#     template_name = 'core/base.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context.update(self.get_context())
#         return context

# class FrontpageView(ContextMixin, TemplateView):
#     template_name = 'core/frontpage.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context.update(self.get_context())
#         return context

# class AboutView(ContextMixin, TemplateView):
#     template_name = 'core/about.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context.update(self.get_context())
#         return context
