from django.contrib import admin
from .models import  *
# Register your models here.


@admin.register(Account)
class AccountModelAdmin(admin.ModelAdmin):
    list_display = ['email','fname','lname','phone','date_of_birth','picture']

@admin.register(StoreModel)
class StoreModelAdmin(admin.ModelAdmin):
    list_display = ['owner','storecategory','storename','gstinno','panno','shopaddress','signature']

@admin.register(MainCategoryModel)
class MainCategoryModelAdmin(admin.ModelAdmin):
    list_display = ['owner','name','image','info']

@admin.register(SubCategoryModel)
class SubCategoryModelAdmin(admin.ModelAdmin):
    list_display = ['owner','name','image','info']


@admin.register(ProductModel)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['owner','store','maincate','subcate','name','og_price','discount','discountedprice','sell_price','image','image1','image2','image3','image4','info','status']