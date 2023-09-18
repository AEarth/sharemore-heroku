from django.shortcuts import render

from store.models import Item, Category
from core.context_processors import navigation

from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from store.models import Item, Category, LendRequest, RequestItems
from store.forms import LendRequestForm
from store.cart import Cart

   
def base(request):
    return render(request, 'core/base.html', {
    })

def frontpage(request):
    return render(request, 'core/frontpage.html', {
    })

def about(request):
    return render(request, 'core/about.html', {
    })

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


