from django.shortcuts import render  
from django.http import HttpResponse   
from .forms import PhotoForm  

def handle_uploaded_file(f):  
    with open('custom/static/upload/'+f.name, 'wb+') as destination:  
        for chunk in f.chunks():  
            destination.write(chunk)  

def index(request):  
    if request.method == 'POST':  
        student = PhotoForm(request.POST, request.FILES)  
        if student.is_valid(): 
            student.save(commit=False)
            student.save() 
            #handle_uploaded_file(request.FILES['file'])  
            return HttpResponse("File uploaded successfuly")  
    else:  
        student = PhotoForm()  
    return render(request,"index.html",{'form':student}) 