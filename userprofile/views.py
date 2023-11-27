from django import forms
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify

from core.context_processors import navigation
from store.forms import ItemForm, LendApproveForm, LendStatusUpdateForm
from store.models import Item, LendRequest, RequestItems, WorkflowState

from .forms import UserprofileForm
from .models import Userprofile


@login_required
def request_detail(request):
    my_requests = LendRequest.objects.filter(requester=request.user, workflow_state=WorkflowState.PENDING)
    their_requests = LendRequest.objects.filter(giver=request.user, workflow_state=WorkflowState.PENDING)
         
    
    if request.method == 'POST':
        # before trying to get instance from database ensure prefix value from post request is valid
        form_prefix = request.POST.get('form_prefix')
        if form_prefix:
            try:
                instance = LendRequest.objects.get(pk=form_prefix)
                approval_form = LendStatusUpdateForm(request.POST, prefix=form_prefix, instance=instance)
 
                        
                if approval_form.is_valid():
                    approval_form.save() #update_fields=['workflow_state', 'status']
                    return redirect('request_detail')
                else:
                    print("form invalid")
    
            except LendRequest.DoesNotExist:
                print(f"LendRequest with pk={form_prefix} does not exist.")
        else:
            print("No form prefix provided.")

    #this form is to approve and possibly adjust dates on a request.

        
        if form_prefix in request.POST:
            approval_form_post = LendStatusUpdateForm(request.POST, prefix=request.POST.get('form_prefix'), instance=LendRequest.objects.get(pk=request.POST.get('form_prefix')))
        
        #approval_form = LendApproveForm(request.POST, prefix=str(their_pending_approval_request.id), instance=their_pending_approval_request)
            if approval_form.is_valid():
                print("form is valid")
                approval_form_post.save(update_fields=['workflow_state', 'status'])
                return redirect('request_detail')
            else:
                print("form invalid")
                    
    

            return redirect('request_detail')
    else:
        print('request.method wasnt post I guess?')
        form = LendApproveForm()
        
    their_pending_requests = LendRequest.objects.filter(giver=request.user, workflow_state=WorkflowState.PENDING)
         
    approval_forms = [LendStatusUpdateForm(prefix=str(their_pending_approval_request.id), instance=their_pending_approval_request) for their_pending_approval_request in their_pending_requests]
 
    
    my_requests = LendRequest.objects.filter(
        Q(requester=request.user, workflow_state=WorkflowState.PENDING) |
        Q(requester=request.user, workflow_state=WorkflowState.APPROVED)
    )
    my_request_forms = [LendStatusUpdateForm(prefix=str(my_request.id), instance=my_request) for my_request in my_requests]
    
    
    context = {
        'my_requests_and_forms': zip(my_requests,my_request_forms),
        'their_pending_request_approval_forms': zip(their_pending_requests, approval_forms),
    }
    
    print("All Context:", context)
    print("their_pending_request_approval_forms:", list(zip(their_pending_requests, approval_forms)))
        
    
    return render(request, 'userprofile/request_details.html', context)



@login_required
def request_strings(request):
        
    approved_string = LendRequest.objects.filter(requester=request.user, workflow_state=WorkflowState.APPROVED)
    denied_string = LendRequest.objects.filter(requester=request.user, workflow_state=WorkflowState.DENIED)
    pending_string = LendRequest.objects.filter(giver=request.user, workflow_state=WorkflowState.PENDING)
    
    context = {
        'approved_string': approved_string,
        'denied_string': denied_string,
        'pending_string': pending_string,
    }
    return render(request, 'userprofile/partials/request_strings.html', context)

@login_required
def request_count_bell(request):
    
    approved_count = LendRequest.objects.filter(requester=request.user, workflow_state=WorkflowState.APPROVED).count()
    denied_count = LendRequest.objects.filter(requester=request.user, workflow_state=WorkflowState.DENIED).count()
    pending_count = LendRequest.objects.filter(giver=request.user, workflow_state=WorkflowState.PENDING).count()
    
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
         
        print(request.POST.get("location_name"))
        
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
    
    # my_received_requests = LendRequest.objects.filter(requester=user, workflow_state=WorkflowState.RECEIVED)
    # borrowed_items=[]
    # for request in my_received_requests:
    #     for request_item in request.request_items.all():
    #         borrowed_items.append(request_item.item)
    
    # IDs of items borrowed by the user
    borrowed_item_ids = RequestItems.objects.filter(
        lend_request__requester=user,
        lend_request__workflow_state=WorkflowState.RECEIVED
    ).values_list('item_id', flat=True)

    # Construct a queryset of borrowed items
    borrowed_items = Item.objects.filter(id__in=borrowed_item_ids)
    
    context = {
     'items': items,
     'borrowed_items': borrowed_items,
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
            item.lat = request.user.userprofile.lat
            item.lon = request.user.userprofile.lon
            item.location_name = request.user.userprofile.location_name
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
            item.lat = request.user.userprofile.lat
            item.lon = request.user.userprofile.lon
            item.location_name = request.user.userprofile.location_name
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