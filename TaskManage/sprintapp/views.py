from django.shortcuts import render,HttpResponse

# Create your views here.


def Sprints(request):
    return render(request,'sprints.html')