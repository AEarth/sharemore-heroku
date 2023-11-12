from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseNotFound, QueryDict
from django.shortcuts import get_object_or_404, redirect, render

from core.context_processors import navigation
from store.cart import Cart
from store.models import Item


def frontpage(request):
    context = {}

    # Search bar
    search = request.GET.get("search") or request.POST.get("search")
    if search and search != "INVALID VAR/EXP: request.GET.search":
        print("Search terms: ", search)
        context["items"] = Item.objects.filter(
            Q(title__icontains=search) | Q(description__icontains=search)
        )
    else:
        context["items"] = Item.objects.filter(is_deleted=False)

    # Paginate the results, assuming you want 6 items per page
    # paginator = Paginator(context["items"], 6)
    # page_number = request.GET.get("page")
    # context["items"] = paginator.get_page(page_number)

    if request.method == "POST":
        print(request.POST)
        if "listview" in request.POST:
            template = "store/item_listview.html"
        elif "gridview" in request.POST:
            template = "store/item_grid.html"

        # Persist the search term across POST requests
        # context["search"] = search

        return render(request, template, context)

    # Persist the search term for initial GET requests
    # context["search"] = search

    return render(request, "core/frontpage.html", context)


def base(request):
    # bell stuff is now in context_processor
    context = {}
    return render(request, "core/base.html", context)


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
#             return render(request, "store/item_listview.html", context)
#         elif "gridview" in request.POST:
#             print(request.POST)
#             return render(request, "store/item_grid.html", context)

#     return render(request, "core/frontpage.html", context)


# if request.htmx:
#     print(request.htmx.current_url)
#     return render(request, 'store/item_listview.html', context)
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
        return render(request, "store/item_listview.html", context)
    else:
        return HttpResponseNotFound()


def about(request):
    context = {}

    return render(request, "core/about.html", context)


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
