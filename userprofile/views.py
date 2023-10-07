from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.contrib import messages

from django import forms


from .models import Userprofile
from store.forms import ItemForm
from store.models import Item, LendRequest, WorkflowState

from core.context_processors import navigation

from .forms import UserprofileForm

from store.forms import LendApproveForm

@login_required
def request_detail(request):
    my_requests = LendRequest.objects.filter(requester=request.user)
    their_requests = LendRequest.objects.filter(giver=request.user)
    
    if request.method == 'POST':
        #this form is to approve and possibly adjust dates on a request.
        for their_request in their_requests:
            if their_request.workflow_state == WorkflowState.PENDING:
                their_pending_approval_request = their_request
                approval_form = LendApproveForm(request.POST, prefix=str(their_pending_approval_request.id), instance=their_pending_approval_request)
                if approval_form.is_valid():
                    approval_form.save()
                    return redirect('request_detail')
                    
        #this form is to confirm the requested item has been received. dates are hidden. 
        for my_request in my_requests:
            if my_request.workflow_state == WorkflowState.APPROVED:
                my_recieve_confirm_request = my_request
                recieve_confirm_form = LendApproveForm(request.POST, prefix=str(my_recieve_confirm_request.id), instance=my_recieve_confirm_request)
                recieve_confirm_form.fields['status'].widget = forms.HiddenInput()
                #recieve_confirm_form['pickup_date'].attrs['readonly'] = True
                #recieve_confirm_form['return_date'].attrs['readonly'] = True
                if recieve_confirm_form.is_valid():
                    recieve_confirm_form.save()
                    return redirect('request_detail')            

            return redirect('request_detail')
    else:
        form = LendApproveForm() 
        
    approval_forms = [LendApproveForm(prefix=str(their_pending_approval_request.id), instance=their_pending_approval_request) for their_pending_approval_request in their_requests]
    
    recieve_confirm_forms = [LendApproveForm(prefix=str(my_recieve_confirm_request.id), instance=my_recieve_confirm_request) for my_recieve_confirm_request in my_requests]
    
    
    context = {
        'my_requests': my_requests,
        'approval_forms': approval_forms,
        'recieve_confirm_forms': recieve_confirm_forms,
        'approval_requests_and_forms': zip(my_requests, approval_forms),
        'recieve_confirm_and_forms': zip(their_requests, recieve_confirm_forms),
    }
    return render(request, 'userprofile/request_details.html', context)

@login_required
def request_strings(request):
        
    approved_string = LendRequest.objects.filter(requester=request.user, status='a')
    denied_string = LendRequest.objects.filter(requester=request.user, status='d')
    pending_string = LendRequest.objects.filter(giver=request.user, status='p')
    
    context = {
        'approved_string': approved_string,
        'denied_string': denied_string,
        'pending_string': pending_string,
    }
    return render(request, 'userprofile/partials/request_strings.html', context)

@login_required
def request_count_bell(request):
    
    approved_count = LendRequest.objects.filter(requester=request.user, status='a').count()
    denied_count = LendRequest.objects.filter(requester=request.user, status='d').count()
    pending_count = LendRequest.objects.filter(giver=request.user, status='p').count()
    
    all_count = approved_count + denied_count + pending_count

    context = {
        'approved_count': approved_count,
        'denied_count': denied_count,
        'pending_count': pending_count,
        'all_count': int(all_count),
    }

    return render(request, 'userprofile/partials/request_count_bell.html', context)

# def update_tasks(request):
#     tasks = Task.objects.all()
    
#     if request.method == 'POST':
#         for task in tasks:
#             form = TaskForm(request.POST, prefix=str(task.id), instance=task)
#             if form.is_valid():
#                 form.save()
#         return redirect('redirect_to_some_view')

#     forms = [TaskForm(prefix=str(task.id), instance=task) for task in tasks]
#     return render(request, 'template_name.html', {'forms': forms, 'tasks': tasks})



def vendor_page(request, pk):
    user = User.objects.get(pk=pk)
    items = user.items.filter(is_deleted=False)
    
    context = {
        'user':user,
        'items': items,
    }
    
    return render(request, 'userprofile/vendor_detail.html', context)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            login(request, user)
            
            user_profile = Userprofile.objects.create(user=user)
            
            return redirect('frontpage')
    else:
        form = UserCreationForm()
    return render(request, 'userprofile/signup.html',{
        'form': form
    })
    
@login_required
def edit_profile(request):
    userprofile = request.user.userprofile
    
    print(request.user.username)
    print(type(request.user.userprofile))
    
    if request.method =='POST':
        form = UserprofileForm(request.POST or None, request.FILES or None, instance=userprofile)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile Updated')
            
            return redirect('myaccount')
        else:
            print(form.errors)
        
    else:
        form = UserprofileForm(instance=userprofile)
            
    context = {
        'form': form,
        'userprofile': userprofile
        }
    return render(request, 'userprofile/edit_profile.html', context)

       
@login_required
def myaccount(request):
    my_profile = request.user.userprofile
    context = {
        'my_profile': my_profile,
    }
    return render(request, 'userprofile/myaccount.html', context)

@login_required
def my_inventory(request):
    user = request.user
    items = request.user.items.exclude(is_deleted=True).all()
    
    context = {
     'items': items,
    }
    return render(request, 'userprofile/my_inventory.html', context)

@login_required
def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        
        if form.is_valid():
            item = form.save(commit=False)
            title = request.POST.get('title')

            item.user = request.user
            item.slug = slugify(title)
            item.save()
            
            messages.success(request, 'Item added!')
            
            return redirect('my_inventory')
    else:
        form = ItemForm()
        
        
    context = {
        'form': form,
         'title': 'Add Item',
         'add_update': 'Add',
    }
    return render(request, 'userprofile/add_item.html', context)

@login_required
def edit_item(request, pk):
    item = Item.objects.filter(user=request.user).get(pk=pk)
    
    if request.method == 'POST':
         form = ItemForm(request.POST or None, request.FILES or None, instance=item)
         if form.is_valid():
             item = form.save(commit=False)
             title = request.POST.get('title')
             item.slug = slugify(title)
             item.save()
             
             #http_response = HttpResponse()
             
             messages.success(request, 'Item updated successfully')
             
             return redirect('my_inventory')
    else:
        form = ItemForm(instance=item)
            
    context = {
        'form': form,
        'item': item,
        'title': 'Edit Item',
        'add_update': 'Update',

    }
    return render(request, 'userprofile/add_item.html', context)

@login_required
def delete_item(request, pk):
    item = Item.objects.filter(user=request.user).get(pk=pk)
    item.is_deleted = True
    item.save()
    messages.success(request, 'Item was deleted')
    
    return redirect('my_inventory')