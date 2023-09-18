from store.models import Item, Category
from userprofile.models import Userprofile


def navigation(request):
        context = {}
        if 'items' not in context:
                context['items'] = Item.objects.filter(is_deleted=False)[0:6]
        context['categories'] = Category.objects.all()
        context['users'] = Userprofile.objects.all()
        return context


# core/context_processors.py

# def navigation(request):
#     context = {}
#     # Add data only if 'items' key doesn't already exist in context
#     if 'items' not in context:
#         context['items'] = SomeModel.objects.all()  # or whatever logic you have
#     return context
