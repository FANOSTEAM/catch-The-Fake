import datetime
from django.shortcuts import render,redirect
from EducationAdmin.models import verification
from verifier.models import Employer
import requests
from random import randint
import traceback
def get_employer_from_session(request):
    if request.session.has_key('username'):
        try:
            username=request.session['username']
            password=request.session['password']
            tin=request.session['tin']
            user=Employer.objects.get(username=username,password=password,owner_tin=tin)
            return user
        except Exception:
            return None
    else:
        return None
def home(request):
    context={}
    return render(request, 'home.html',context)
def login(request):
    if get_employer_from_session(request) != None:
        return redirect('employerIndex')
    else:
        if request.method=='POST':
            username=request.POST['username']
            password=request.POST['password']
            remember=request.POST['remember']
            # try:
            employer=Employer.objects.get(username=username,password=password)
            request.session['username']=username
            request.session['password']=password
            request.session['tin']=employer.owner_tin
            if remember=='true':
                pass
            else:
                request.session.set_expiry(0)
            request.modified=True
            return redirect('employerIndex')
            # except Exception:
            #     return redirect('login')
        else:
            context={}
            return render(request, 'login.html',context)
def signup(request):
    context={}
    return render(request, 'signup.html',context)
def tin(request):

    if request.method =='POST':
        tin=request.POST['TIN']
        username=request.POST['username']
        password=request.POST['password']
        email=request.POST['email']
        response = requests.get(f'http://127.0.0.1:8000/{tin}').json()
        if 'phone' in response:
            request.session['username']=username
            request.session['password']=password
            request.session['tin']=tin
            try:
                employer=Employer.objects.get(owner_tin=tin)
                if employer.verified:
                    return redirect('login')
                else:
                    v=verification.objects.create(creation_date=datetime.datetime.now(),
                                             expiration_date=datetime.datetime.now()+datetime.timedelta(days=1),
                                             code=randint(20000,70000))
                    try:
                        code=employer.code
                        employer.code=v
                        v.employer=employer
                        v.save()
                        employer.save()
                        code.employer=None
                        code.save()
                        code.delete()
                        print(v.code)
                        #code.delete()
                        context={'code':employer}
                        #print(employer.id)
                        return render(request, 'signup.html',context)
                    except Exception as exc:
                        traceback.print_exc()
                        return None
                        
            except Exception:
                
                code=verification.objects.create(creation_date=datetime.datetime.now(),
                                             expiration_date=datetime.datetime.now()+datetime.timedelta(days=1),
                                             code=randint(20000,70000))
                employer=Employer(username=username,password=password,email=email,owner_tin=tin,verified=False,code=code)
                employer.save()
            print(str(code)+'\n'+f'code:{code.code} code was sent to {employer.email}')
            context={'code':employer}
            return render(request, 'signup.html',context)
        else:
            context={'notin':True}
            return render(request, 'signup.html',context)
    else:
        return redirect('signup')
def code(request):
    if get_employer_from_session(request)!=None:
        user=get_employer_from_session(request)
        if request.method=='POST':
            code=request.POST['code']
            c=user.code
            if user.code.code==int(code):
                user.verified=True
                user.code=None
                user.save()
                c.employer=None
                c.save()
                c.delete()
                return redirect('employerIndex')
            else:
                return render(request,'signup.html',{'code':user})
    else:
        return redirect('login')
def signout(request):
    if get_employer_from_session(request)!=None:
        request.session.flush()
        return redirect('login')
    else:
        return redirect('login')