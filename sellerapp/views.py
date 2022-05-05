from django.shortcuts import redirect, render
from .form import *
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required, permission_required,user_passes_test
# Create your views here.

def SignupView(request):
    if request.method == 'POST':

        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = SignupForm()
            
    context = {'form':form}
    return render(request,'signup.html',context)

def SigninView(request):
    form = SigninForm()
    if request.method == 'POST':
        uname = request.POST['username']
        upass = request.POST['password']
        # print(uname,upass)
        user = authenticate(email=uname, password=upass)
        
        if user is None:
            # print(user)
            messages.error(request, 'Please Enter Correct Credinatial')
            
            return redirect('/seller/')
        else:
            login(request, user)
            if request.user.is_superuser:
                print(request.user)
                messages.success(request, f'{request.user} - Login Successful')
                return redirect('/admin/admindash/')
            if request.user.is_seller:
                login(request, user)
                messages.success(request, f'{request.user} - Login Successful')
                return redirect('/seller/managestore/')
    else:
        # if request.user.is_authenticated:
        #     return redirect('/seller/managestore/')
        
        return render(request, 'signin.html',{'form':form})

# Seller Profile Update
def ProfileView(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST,request.FILES,instance=request.user)
        if form.is_valid():
            
            form.save()
            messages.info(request, 'Profile Successfully Updated')
            return redirect('/seller/profile/')

    else:
        form = ProfileForm(instance=request.user)
    context = {'form':form}
    return render(request,'sellerprofile.html',context)

# Logout
def Userlogout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, 'You are Successfully Logged Out !')
    return redirect('/seller/')

@login_required
@user_passes_test(lambda u: u.is_seller)
def SellerDashbordView(request):
    all_stores = StoreModel.objects.filter(owner=request.user)
    
    
    active_store_count = [i for i in  StoreModel.objects.filter(owner=request.user) if i.status == True]
    
    sname = request.GET.get('sname')
    if sname:
        all_stores = StoreModel.objects.filter(owner=request.user,storename__icontains=sname)
    context = {'all_stores':all_stores,'active_store_count':len(active_store_count)}
    return render(request,'sellerdash.html',context)

@login_required
@user_passes_test(lambda u: u.is_seller)
def AddStoreView(request):
    if request.method == 'POST':
        form = AddStoreForm(request.POST,request.FILES,label_suffix='')
        if form.is_valid():
            sttname = form.cleaned_data['storename']
            fm = form.save(commit=False)
            fm.owner = request.user
            fm.save()
            messages.success(request,f' {sttname} - Store Added Successfully')
            return redirect('/seller/addstore/')
    else:
        form = AddStoreForm(label_suffix='')
    context = {'form':form}
    return render(request,'addstore.html',context)

# ---------- Store CRUD Start ----------
@login_required
@user_passes_test(lambda u: u.is_seller)
def ManageStoreView(request):
    all_stores = StoreModel.objects.filter(owner=request.user)
    context = {'all_stores':all_stores}
    return render(request,'managestore.html',context)

@login_required
@user_passes_test(lambda u: u.is_seller)
def DeleteStoreView(request,id):
    get_store = StoreModel.objects.get(id=id)
    get_store.delete()
    messages.error(request, 'Store Successfully Deleted !')
    return redirect('/seller/managestore/')

@login_required
@user_passes_test(lambda u: u.is_seller)
def UpdateStoreView(request,id):
    if request.method == 'POST':
        get_store = StoreModel.objects.get(id=id)
        form = AddStoreForm(request.POST,request.FILES,instance=get_store)
        if form.is_valid():
            form.save()
            messages.info(request, 'Store Successfully Updated !')
            return redirect('/seller/managestore/')

    else:
        get_store = StoreModel.objects.get(id=id)
        form = AddStoreForm(instance=get_store)
    context = {'form':form}
    return render(request,'addstore.html',context)


# ---------- Product CRUD Start ----------
@login_required
@user_passes_test(lambda u: u.is_seller)
def AddProductsView(request,id):
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES,label_suffix='')
        if form.is_valid():
            pname = form.cleaned_data['name']
            fm = form.save(commit=False)
            fm.owner = request.user
            fm.store = StoreModel.objects.get(id=id)
            fm.save()
            messages.success(request,f' {pname} - Product Added Successfully')
            return redirect('/seller/addstore/')
    else:
        form = ProductForm(label_suffix='')
    context = {'form':form}
    return render(request,'addproduct.html',context)

@login_required
@user_passes_test(lambda u: u.is_seller)
def UpdateProductView(request,id):
    if request.method == 'POST':
        get_store = ProductModel.objects.get(id=id)
        form = ProductForm(request.POST,request.FILES,instance=get_store)
        if form.is_valid():
            form.save()
            messages.info(request, 'Product Successfully Updated !')
            # return redirect('/seller/storedetails/')
            context = {'form':form}
            return render(request,'addproduct.html',context)

    else:
        get_store = ProductModel.objects.get(id=id)
        form = ProductForm(instance=get_store)
    context = {'form':form}
    return render(request,'addproduct.html',context)

@login_required
@user_passes_test(lambda u: u.is_seller)
def StoreDetailsView(request,id):
    show_products = ProductModel.objects.filter(owner=request.user,store=id)
    
    get_mcat = [i.name for i in MainCategoryModel.objects.filter(owner=request.user)]
    get_scat = [i.name for i in SubCategoryModel.objects.filter(owner=request.user)]
    mcate = request.GET.get('mcate')
    scate = request.GET.get('scate')
    pname = request.GET.get('pname')
    if mcate and scate and pname:
        show_products = ProductModel.objects.filter(owner=request.user,store=id,maincate__name__icontains=mcate,subcate__name__icontains=scate,name__icontains=pname)
    if mcate and scate == '' and pname == '' :
        show_products = ProductModel.objects.filter(owner=request.user,store=id,maincate__name__icontains=mcate,)
    if mcate == '' and scate == '' and pname:
        show_products = ProductModel.objects.filter(owner=request.user,store=id,name__icontains=pname)
    if mcate == '' and scate and pname == '':
        show_products = ProductModel.objects.filter(owner=request.user,store=id,subcate__name__icontains=scate)
    context = {'show_products':show_products,'sroreid':id,'get_mcat':get_mcat,'get_scat':get_scat}
    return render(request,'storedetails.html',context)

