from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.http import request
from django.utils import timezone

# User Coutom Manager
class AccountManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email,name, fname,lname, phone, password, **extra_fields):
        values = [email, fname,lname, phone]
        field_value_map = dict(zip(self.model.REQUIRED_FIELDS, values))
        for field_name, value in field_value_map.items():
            if not value:
                raise ValueError('The {} value must be set'.format(field_name))

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            name=name,
            fname=fname,
            lname=lname,
            phone=phone,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email,name, fname,lname, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email,name, fname,lname, phone, password, **extra_fields)

    def create_superuser(self, email,name, fname,lname, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email,name, fname,lname, phone, password, **extra_fields)


    # ------------ For Create Staff User  ------------
    # def create_staffuser(self, email, password):
    #     """
    #     Creates and saves a staff user with the given email and password.
    #     """
    #     user = self.create_user(
    #         email,
    #         password=password,
    #     )
    #     user.staff = True
    #     user.save(using=self._db)
    #     return user

# User Model
class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=150)
    fname = models.CharField(max_length=150)
    lname = models.CharField(max_length=150)
    phone = models.CharField(max_length=50)
    date_of_birth = models.DateTimeField(blank=True, null=True)
    picture = models.ImageField(blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_seller = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True)
    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','fname','lname','phone']

    def get_full_name(self):
        return self.fname

    def get_short_name(self):
        return self.fname.split()[0]

# Store Model
stcategory = (('Electronics','Electronics'),('Grocery','Grocery'),('Cloths','Cloths'))

class StoreModel(models.Model):
    owner = models.ForeignKey(Account,on_delete=models.CASCADE)
    storecategory = models.CharField(max_length=200,choices=stcategory)
    storelogo = models.ImageField(upload_to = 'Storelogo',null=True,blank=True)
    storename = models.CharField(max_length=200)
    city_name = models.CharField(max_length=200)
    pincodeno = models.IntegerField()
    gstinno = models.CharField(max_length=200)
    panno = models.CharField(max_length=200)
    shopaddress = models.TextField()
    signature = models.ImageField(upload_to = 'Storedetail')
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.storename

    
    @property   
    def total_quantity(self):
        return ProductModel.objects.filter(store=self.id).count()

    @property
    def active_store(self):
        return StoreModel.objects.filter(store=self.id,status=True).count()

# Main Category of Product
class MainCategoryModel(models.Model):
    owner = models.ForeignKey(Account,on_delete=models.CASCADE)
    # store = models.ForeignKey(StoreModel,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to = 'Maincategory')
    info = models.CharField(max_length=200)

    def __str__(self):
        return self.name

# Sub Category of Product
class SubCategoryModel(models.Model):
    owner = models.ForeignKey(Account,on_delete=models.CASCADE)
    # store = models.ForeignKey(StoreModel,on_delete=models.CASCADE)
    # mcate = models.ForeignKey(MainCategoryModel,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to = 'Subcategory')
    info = models.CharField(max_length=200)

    def __str__(self):
        return self.name

# Product Model
pstatus = (('Frash Arrival','Frash Arrival'),('Trending','Trending'),('Out of Stock','Out of Stock'))
class ProductModel(models.Model):
    owner = models.ForeignKey(Account,on_delete=models.CASCADE)
    store = models.ForeignKey(StoreModel,on_delete=models.CASCADE)
    maincate = models.ForeignKey(MainCategoryModel,on_delete=models.CASCADE)
    subcate = models.ForeignKey(SubCategoryModel,on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=200)
    og_price = models.IntegerField(default=0)
    discount = models.IntegerField(default=0)
    discountedprice = models.IntegerField(default=0)
    sell_price = models.IntegerField(default=0)
    image = models.ImageField(upload_to = 'Product')
    image1 = models.ImageField(upload_to = 'Product',null=True,blank=True)
    image2 = models.ImageField(upload_to = 'Product',null=True,blank=True)
    image3 = models.ImageField(upload_to = 'Product',null=True,blank=True)
    image4 = models.ImageField(upload_to = 'Product',null=True,blank=True)
    info = models.CharField(max_length=200)
    status = models.CharField(choices=pstatus,max_length=200,default='Frash Arrival')

    

    def dis_price(self):
        return (self.og_price*self.discount)/100

    def sll_price(self):
        return(self.og_price - self.dis_price())

    

    def save(self, *args, **kwargs):
        self.sell_price = self.sll_price()
        self.discountedprice = self.dis_price()
        super(ProductModel, self).save(*args, **kwargs)

    
        # return ProductModel.objects.filter(maincate=[i.id for i in MainCategoryModel])