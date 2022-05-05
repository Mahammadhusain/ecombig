from django.shortcuts import render
from sellerapp.models import MainCategoryModel
# Create your views here.
def HomeView(request):
    all_mcate = MainCategoryModel.objects.all()
    
    context = {'all_mcate':all_mcate}
    return render(request,'index.html',context)