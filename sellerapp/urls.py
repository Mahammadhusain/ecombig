from django.urls import path
from .views import *

urlpatterns = [
    path('', SigninView),
    path('signup/', SignupView,name='signup'),
    path('out/', Userlogout),
    path('sellerdash/', SellerDashbordView,name='sellerdash'),

    # Stor Manage

    path('profile/', ProfileView,name='profile'),
    path('addstore/', AddStoreView,name='addstore'),
    path('managestore/', ManageStoreView,name='managestore'),
    path('deletestore/<int:id>/', DeleteStoreView,name='deletestore'),
    path('updatestore/<int:id>/', UpdateStoreView,name='updatestore'),

    # Product manage
    path('addproducts/<int:id>/', AddProductsView,name='addproducts'),
    path('updateproducts/<int:id>/', UpdateProductView,name='updateproducts'),
    path('storedetails/<int:id>/', StoreDetailsView,name='storedetails'),
]
