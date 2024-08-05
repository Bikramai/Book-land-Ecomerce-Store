from django.urls import path

from src.administration.client.views import ClientDashboard, WishlistView, WishListDelete, UserUpdateView, \
    AddressUpdate, WishCreateView, OrderListView, AddressList, BooksListView, download_file,ReadBook

app_name = 'client'
urlpatterns = [
    path('', ClientDashboard.as_view(), name='dashboard'),

    path('wishlist/', WishlistView.as_view(), name='wishlist'),
    path('wishlist/create/<str:pk>', WishCreateView.as_view(), name='wishlist-create'),
    path('wishlist/delete/<str:pk>', WishListDelete.as_view(), name='wishlist-delete'),

    path('my-orders/', OrderListView.as_view(), name='order_list'),
    path('my-address/', AddressList.as_view(), name='address'),
    path('my-books/', BooksListView.as_view(), name='book'),

    path('user/change/', UserUpdateView.as_view(), name='user-change'),
    path('user/address/update/<str:pk>', AddressUpdate.as_view(), name='user-address-update'), #not known

    path('download-file/<str:pk>', download_file, name='download_file'),
    path('read/book/<str:pk>', ReadBook.as_view(), name='read_book'),

]
