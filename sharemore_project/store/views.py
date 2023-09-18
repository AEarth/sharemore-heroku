from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Item, Category, LendRequest, RequestItems
from .forms import LendRequestForm
from .cart import Cart


@login_required
def lend_request(request):
    cart = Cart(request)
    
    
    if request.method == 'POST':
        form = LendRequestForm(request.POST)
        if form.is_valid():
            
            all_givers = []
            for item in cart:
                indv_item = item['item']
                #check to see if requesting to multiple people simultaniously
                if indv_item.user not in all_givers:
                    all_givers.append(indv_item.user)
                    
                if indv_item.user == request.user:
                    messages.error(request, 'You cannot request to borrow your own items')
                    return redirect('cart_view')
                
            if len(all_givers) > 1:
                messages.error(request, 'You cannot request to borrow items from multiple people at once')
                return redirect('cart_view')
            
            total_value = 0
            
            for item in cart:
                indv_item = item['item']
                total_value += indv_item.value * int(item['quantity'])
                
            lend_request = form.save(commit=False)
            lend_request.requester = request.user
            lend_request.giver = indv_item.user
            lend_request.status = 'p'
            lend_request.save()
            
            for item in cart:
                indv_item = item['item']
                quantity = item['quantity']
                RequestItems.objects.create(lend_request=lend_request, item=indv_item, value=indv_item.value, quantity=quantity)
                
            cart.clear()
            
            return redirect('myaccount')
    else:
        form = LendRequestForm() 
    context = {
        'cart': cart,
        'form': form,
        }
    return render(request, 'store/lend_request.html', context)


def change_quantity(request, item_id):
    action = request.GET.get('action', '')
    cart = Cart(request)
    
    if action:
        quantity = 1
        
        if action == 'decrease':
            quantity = -1
        
        cart.add(item_id, quantity, update_quantity=True)

    return redirect('cart_view')

def remove_from_cart(request, item_id):
    cart = Cart(request)
    cart.remove_item(item_id)
    
    return redirect('cart_view')

def add_to_cart(request, item_id):
    cart = Cart(request)
    cart.add(item_id)
    
    return redirect('frontpage')

def cart_view(request):
    cart = Cart(request)
    for item in cart:
            indv_item = item['item']
    context = {'cart': cart}
    return render(request, 'store/cart_view.html', context)

def search(request):
    query = request.GET.get('query', '')
    items = Item.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    context = {
        'query': query,
        'items': items,
    }
    return render(request, 'store/search.html', context)


def item_detail(request, category_slug, slug):
    item = get_object_or_404(Item,slug=slug, is_deleted=False)
    cart = Cart(request)
    # print(cart.get_total_cost())
    
    context = {
        'item': item,
    }
    return render(request, 'store/item_detail.html', context)


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    items = category.items.exclude(is_deleted=True).all()
    
    context =  {
        'category': category,
        'items': items,
    }
    return render(request, 'store/category_detail.html', context)

