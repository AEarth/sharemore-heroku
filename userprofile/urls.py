from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='userprofile/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('vendors/<int:pk>/', views.vendor_page, name='vendor_page'),
    path('myaccount/', views.myaccount, name='myaccount'),
    path('myaccount/requests/', views.request_detail, name='request_detail'),
    path('myaccount/requests/count_bell/', views.request_count_bell, name='request_count_bell'),
    path('myaccount/requests/strings/', views.request_strings, name='request_strings'),
    # path('myaccount/their_requests/', views.their_request_detail, name='their_request_detail'),
    path('myaccount/edit', views.edit_profile, name='edit_profile'),
    path('my-inventory/', views.my_inventory, name='my_inventory'),
    path('my-inventory/add-item/', views.add_item, name='add_item'),
    path('my-inventory/edit-item/<int:pk>/', views.edit_item, name='edit_item'),
    path('my-inventory/delete-item/<int:pk>/', views.delete_item, name='delete_item'),
]
