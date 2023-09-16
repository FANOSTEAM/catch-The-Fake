from django.shortcuts import render

def index(request):
    context={}
    return render(request, "EducationAdmin/index.html",context)