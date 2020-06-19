from django.shortcuts import render

# Create your views here.
def show(request):
    return render(request,'showdiary.html')

def add (request):
    if request.method=="POST":
        return render (request,'showdiary.html')
    else:
        return render(request,'Add memory.html')