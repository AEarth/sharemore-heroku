from django.urls import path

from . import views

urlpatterns = [
    path('search/', views.search, name='search'),
    path('add_to_cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('change-quantity/<str:item_id>/', views.change_quantity, name='change_quantity'),
    path('remove_from_cart/<str:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/lend_request/', views.lend_request, name='lend_request'),
    path('<slug:slug>/', views.category_detail, name='category_detail'),
    path('<slug:category_slug>/<slug:slug>/', views.item_detail, name='item_detail'),

]