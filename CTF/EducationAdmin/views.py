from django.http import FileResponse
from django.shortcuts import render , redirect
from EducationAdmin.models import Collage, Major, Title, University
from EducationAdmin.models import AdminUser
from Student.models import Certificate
from .forms import UploadImageForm
from tablib import Dataset
def get_admin_user(request):
    if request.session.has_key('AdminUser') and request.session.has_key('AdminPassword'):
        try:
            username=request.session['AdminUser']
            password=request.session['AdminPassword']
            adminUser=AdminUser.objects.get(userName=username,password=password)
            return adminUser
        except Exception:
            return None
    else:
        return None
def index(request):
    if get_admin_user(request)!=None:
        adminUser=get_admin_user(request)

        context={'adminUser':adminUser}
        return render(request, "EducationAdmin/index.html",context)
    else:
        return redirect('adminLogin')
def login(request):
    if get_admin_user(request)!=None:
        adminUser=get_admin_user(request)

        context={'adminUser':adminUser}
        return redirect("AdminIndex")
    else:
        if request.method=='POST':
            username=request.POST['username']
            password=request.POST['password']
            remember=request.POST['remember']
            try:
                admin=AdminUser.objects.get(userName=username,password=password)
                request.session['AdminUser']=username
                request.session['AdminPassword']=password
                print(remember)
                if remember=='true':
                    pass
                else:
                    request.session.set_expiry(0)
                request.session.modified=True
                return redirect('AdminIndex')
            except Exception:
                
                context ={'err':True}
                return render(request,'EducationAdmin/login.html',context)
        else:
            context ={}
            return render(request,'EducationAdmin/login.html',context)
def gallery_with_upload(request):
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            xls=request.Files['excel']
            for image in request.FILES.getlist('images'):
                Certificate.objects.create(profile_picture=image)
    else:
        form = UploadImageForm()
    gallery = Certificate.objects.all()
    return render(request, 'gallery_with_upload.html', {'form': form, 'gallery': gallery})
def upload(request):
    if get_admin_user(request)!=None:
        if request.method=='POST':
            profiles=request.FILES.getlist("files")
            excel= request.FILES.get('excel')
            if excel!=None:
                data=Dataset()
                dataset=data.load(excel.read())
                for row in dataset.dict:
                    firstName=row['first Name']
                    middleName=row['middle Name']
                    lastName=row['last Name']
                    UniversityId=row['University Id']
                    GPA=row['GPA']
                    CGPA=row['CGPA']
                    majorName=row['Major']
                    Degree=row['Degree']
                    DATE=row['date']
                    collageName=row['Collage ID']
                    profile_picture_id=row['profileId']
                    type_of_certificate=row['type_of_certificate']
                    print(firstName,middleName,lastName,collageName,UniversityId,GPA,CGPA,DATE,Degree,majorName,profile_picture_id)
                    for i in profiles:
                        if(i.name[:i.name.index('.')]==profile_picture_id):
                            profile=i
                            print('yesp')
                        else:
                            print('no')
                            continue
                        # try:
                        university=University.objects.get(UniversityId=UniversityId)
                        collage=Collage.objects.get(name=collageName,university=university)
                        major=Major.objects.get(collage=collage,name=
                                                majorName)
                        title=Title.objects.get(major=major,title=Degree)
                        cetificate=Certificate(firstName=firstName,middleName=middleName,lastName=lastName,GPA=GPA,CGPA=CGPA,title=title,profile_picture=profile,school=collage,ban=False,issued_on=DATE,type_of_certificate=type_of_certificate)
                        cetificate.save()
                        print('yes')
                        
                        # except Exception:
                        #     print('error')
                        #     continue
                        

        else:
            return None
    else:
        return redirect('login')
def adminSignout(request):
    if get_admin_user(request)!=None:
        request.session.flush()
        return redirect('adminLogin')
    else:
        return redirect('adminLogin')
def universities(request):
    if get_admin_user(request)!=None:
        adminUser=get_admin_user(request)
        universities=University.objects.all()
        context={'adminUser':adminUser,'universities':universities}
        return render(request,'EducationAdmin/universities.html',context)
    else:
        return redirect('adminLogin')
def universitiesEdit(request):
    if get_admin_user(request)!=None:
        if request.method=='POST':
            adminUser=get_admin_user(request)
            university_id=request.POST.get('universityId')
            university_name=request.POST.get('universityName')
            logo=request.FILES.get('logo')
            id=int(request.POST.get('buffer'))
            
            print(university_name,university_id,logo.read())

            university=University.objects.get(id=id)
            university.name=university_name
            university_id=university_id
            university.logo=logo.read()
            university.save()
            print('success')
            universities=University.objects.all()
            context={'adminUser':adminUser,'universities':universities}
            return render(request,'EducationAdmin/universities.html',context)
    else:
        return redirect('adminLogin')