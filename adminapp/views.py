from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required,user_passes_test

# Create your views here.
@login_required
@user_passes_test(lambda u: u.is_admin)
def AdminDashbordView(request):
    
    return render(request,'admindash.html')