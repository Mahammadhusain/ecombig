from django import forms
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm



# Adding New Store Form
class AddStoreForm(forms.ModelForm):
    
    class Meta:
        model = StoreModel
        fields="__all__"
        exclude = ['owner','status']
        widgets ={
            'storecategory':forms.Select(attrs={'class':'form-control'}),
            'storename':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Store Name'}),
            'storelogo':forms.FileInput(attrs={'class':'form-control','placeholder':'Upload Store Logo'}),
            'gstinno':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter GST No'}),
            'panno':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter PAN No'}),
            'shopaddress':forms.Textarea(attrs={'class':'form-control','placeholder':'Enter Store Address'}),
            'signature':forms.FileInput(attrs={'class':'form-control'}),
            'city_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter City Name'}),
            'pincodeno':forms.NumberInput(attrs={'class':'form-control','placeholder':'Enter Pincode No3'}),
            # 'status':forms.CheckboxInput(attrs={'class':'form-check-input',}),
        }



# Adding New Products Form
class ProductForm(forms.ModelForm):
    
    class Meta:
        model = ProductModel
        fields="__all__"
        exclude = ['owner','store','discountedprice','sell_price']
        widgets ={
            'maincate':forms.Select(attrs={'class':'form-control'}),
            'subcate':forms.Select(attrs={'class':'form-control'}),
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Store Name'}),
            'og_price':forms.NumberInput(attrs={'class':'form-control','placeholder':'Upload Store Logo'}),
            'discount':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter GST No'}),
            'image':forms.FileInput(attrs={'class':'form-control','placeholder':'Enter PAN No'}),
            'image1':forms.FileInput(attrs={'class':'form-control','placeholder':'Enter PAN No'}),
            'image2':forms.FileInput(attrs={'class':'form-control','placeholder':'Enter PAN No'}),
            'image3':forms.FileInput(attrs={'class':'form-control','placeholder':'Enter PAN No'}),
            'image4':forms.FileInput(attrs={'class':'form-control','placeholder':'Enter PAN No'}),
            'info':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Store Address'}),
            'status':forms.Select(attrs={'class':'form-control',}),
        }


class ProfileForm(forms.ModelForm):
    
    class Meta:
        model = Account
        fields = ['email','name','fname','lname','phone','date_of_birth','picture']

        widgets ={
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'fname':forms.TextInput(attrs={'class':'form-control'}),
            'lname':forms.TextInput(attrs={'class':'form-control'}),
            'phone':forms.NumberInput(attrs={'class':'form-control'}),
            'picture':forms.FileInput(attrs={'class':'form-control'}),
            'date_of_birth':forms.DateTimeInput(attrs={'class':'form-control','type':'datetime-local'}),
        }













# --------------------------------- AUTH SECTION ---------------------------   
# User Signup
class SignupForm(UserCreationForm):
    password1 = forms.CharField( widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Password'}))
    password2 = forms.CharField( widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm Password'}))
    class Meta:
        model = Account
        fields = ['email','name','fname','lname','phone','date_of_birth','password1','password2','picture']

        widgets ={
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter E-Mail'}),
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Name'}),
            'fname':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Firstname'}),
            'lname':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Lastname'}),
            'phone':forms.NumberInput(attrs={'class':'form-control','placeholder':'Enter Mobile No'}),
            'picture':forms.FileInput(attrs={'class':'form-control'}),
            'date_of_birth':forms.DateTimeInput(attrs={'class':'form-control','type':'datetime-local'}),
        }

        



# User Signin
class SigninForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter E-Mail'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Password'}))

    class Meta:
        model = User
        fields = ['username','password']