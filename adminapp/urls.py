from django.urls import path
from .views import *

urlpatterns = [
    
    path('admindash/', AdminDashbordView,name='admindash'),

]