from django.http import FileResponse, HttpResponseNotFound, JsonResponse
from django.shortcuts import redirect, render
from EducationAdmin.models import AdminUser, Collage, Major, Title, University
from Student.models import Certificate
from tablib import Dataset

from .forms import UploadImageForm


def get_admin_user(request):
    if request.session.has_key("AdminUser") and request.session.has_key(
        "AdminPassword"
    ):
        try:
            username = request.session["AdminUser"]
            password = request.session["AdminPassword"]
            adminUser = AdminUser.objects.get(userName=username, password=password)
            return adminUser
        except Exception:
            return None
    else:
        return None


def index(request):
    if get_admin_user(request) != None:
        adminUser = get_admin_user(request)

        context = {"adminUser": adminUser}
        return render(request, "EducationAdmin/index.html", context)
    else:
        return redirect("adminLogin")


def login(request):
    if get_admin_user(request) != None:
        adminUser = get_admin_user(request)

        context = {"adminUser": adminUser}
        return redirect("AdminIndex")
    else:
        if request.method == "POST":
            username = request.POST["username"]
            password = request.POST["password"]
            remember = request.POST["remember"]
            try:
                admin = AdminUser.objects.get(userName=username, password=password)
                request.session["AdminUser"] = username
                request.session["AdminPassword"] = password
                print(remember)
                if remember == "true":
                    pass
                else:
                    request.session.set_expiry(0)
                request.session.modified = True
                return redirect("AdminIndex")
            except Exception:
                context = {"err": True}
                return render(request, "EducationAdmin/login.html", context)
        else:
            context = {}
            return render(request, "EducationAdmin/login.html", context)


def gallery_with_upload(request):
    if request.method == "POST":
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            xls = request.Files["excel"]
            for image in request.FILES.getlist("images"):
                Certificate.objects.create(profile_picture=image)
    else:
        form = UploadImageForm()
    gallery = Certificate.objects.all()
    return render(
        request, "gallery_with_upload.html", {"form": form, "gallery": gallery}
    )


def upload(request):
    if get_admin_user(request) != None:
        if request.method == "POST":
            profiles = request.FILES.getlist("files")
            excel = request.FILES.get("excel")
            uploaded = dict()
            invalids = dict()
            if excel != None:
                data = Dataset()
                dataset = data.load(excel.read())
                for row in dataset.dict:
                    firstName = row["first Name"]
                    middleName = row["middle Name"]
                    lastName = row["last Name"]
                    UniversityId = row["University Id"]
                    GPA = row["GPA"]
                    CGPA = row["CGPA"]
                    majorName = row["Major"]
                    Degree = row["Degree"]
                    DATE = row["date"]
                    collageName = row["Collage ID"]
                    profile_picture_id = row["profileId"]
                    type_of_certificate = row["type_of_certificate"]
                    print(
                        firstName,
                        middleName,
                        lastName,
                        collageName,
                        UniversityId,
                        GPA,
                        CGPA,
                        DATE,
                        Degree,
                        majorName,
                        profile_picture_id,
                    )
                    for i in profiles:
                        if i.name[: i.name.index(".")] == profile_picture_id:
                            profile = i
                            print("yesp")
                        else:
                            print("no")
                            continue
                        try:
                            university = University.objects.get(
                                UniversityId=UniversityId
                            )
                            collage = Collage.objects.get(
                                name=collageName, university=university
                            )
                            major = Major.objects.get(collage=collage, name=majorName)
                            title = Title.objects.get(major=major, title=Degree)
                            cetificate = Certificate(
                                firstName=firstName,
                                middleName=middleName,
                                lastName=lastName,
                                GPA=GPA,
                                CGPA=CGPA,
                                title=title,
                                profile_picture=profile,
                                school=collage,
                                ban=False,
                                issued_on=DATE,
                                type_of_certificate=type_of_certificate,
                            )

                            cetificate.save()
                            uploaded[profiles.index(i)] = [
                                firstName,
                                middleName,
                                lastName,
                            ]

                        except Exception:
                            print("error")
                            invalids[profiles.index(i)] = [
                                firstName,
                                middleName,
                                lastName,
                            ]
                            continue
                return JsonResponse({"invalids": invalids, "uploaded": uploaded})
        else:
            return None
    else:
        return redirect("login")


def adminSignout(request):
    if get_admin_user(request) != None:
        request.session.flush()
        return redirect("adminLogin")
    else:
        return redirect("adminLogin")


def universities(request):
    if get_admin_user(request) != None:
        adminUser = get_admin_user(request)
        universities = University.objects.all()
        context = {"adminUser": adminUser, "universities": universities}
        return render(request, "EducationAdmin/universities.html", context)
    else:
        return redirect("adminLogin")


def universitiesEdit(request):
    if get_admin_user(request) != None:
        if request.method == "POST":
            adminUser = get_admin_user(request)
            university_id = request.POST.get("universityId")
            university_name = request.POST.get("universityName")
            logo = request.FILES.get("logo")
            id = int(request.POST.get("buffer"))

            print(university_name, university_id, logo)
            university = University.objects.get(id=id)
            university.name = university_name
            university.UniversityId = university_id
            university.logo = logo
            university.save()
            print("success")
            universities = University.objects.all()
            context = {"adminUser": adminUser, "universities": universities}
            return render(request, "EducationAdmin/universities.html", context)
    else:
        return redirect("adminLogin")


def collage(request, collage_id):
    if get_admin_user(request) != None:
        adminUser = get_admin_user(request)
        try:
            university = University.objects.get(id=collage_id)
            collages = university.collage_set.all()
        except University.DoesNotExist():
            return FileNotFoundError()

        context = {"adminUser": adminUser, "collages": collages}
        return render(request, "EducationAdmin/collages.html", context)
    return redirect("adminLogin")


def major(request, collage_id):
    if get_admin_user(request) != None:
        adminUser = get_admin_user(request)
        try:
            collage = Collage.objects.get(id=collage_id)
            majors = collage.major_set.all()
        except Collage.DoesNotExist():
            return FileNotFoundError()

        context = {"adminUser": adminUser, "majors": majors}
        return render(request, "EducationAdmin/major.html", context)
    return redirect("adminLogin")


def degree(request, major_id):
    if get_admin_user(request) != None:
        adminUser = get_admin_user(request)
        try:
            major = Major.objects.get(id=major_id)
            titles = major.title_set.all()
        except Collage.DoesNotExist():
            return FileNotFoundError()

        context = {"adminUser": adminUser, "titles": titles}
        return render(request, "EducationAdmin/title.html", context)
    return redirect("adminLogin")


def collage_edit(request):
    if get_admin_user(request) != None:
        if request.method == "POST":
            adminUser = get_admin_user(request)

            collage_name = request.POST.get("collage_name")

            id = int(request.POST.get("buffer"))

            collage = Collage.objects.get(id=id)
            collage.name = collage_name

            collage.save()
            print("success")
            collages = Collage.objects.all()
            context = {"adminUser": adminUser, "collages": collages}
            return render(request, "EducationAdmin/collages.html", context)
    else:
        return redirect("adminLogin")


def major_edit(request):
    if get_admin_user(request) != None:
        if request.method == "POST":
            adminUser = get_admin_user(request)

            major_name = request.POST.get("major_name")

            id = int(request.POST.get("buffer"))

            major = Major.objects.get(id=id)
            major.name = major_name

            major.save()
            print("success")
            majors = major.objects.all()
            context = {"adminUser": adminUser, "majors": majors}
            return render(request, "EducationAdmin/major.html", context)
    else:
        return redirect("adminLogin")


def degree_edit(request):
    if get_admin_user(request) != None:
        if request.method == "POST":
            adminUser = get_admin_user(request)

            degree_name = request.POST.get("title")

            id = int(request.POST.get("buffer"))

            title = Title.objects.get(id=id)
            title.title = degree_name
            title.save()
            print("success")
            titles = Title.objects.all()
            context = {"adminUser": adminUser, "titles": titles}
            return render(request, "EducationAdmin/major.html", context)
    else:
        return redirect("adminLogin")


def certificates(request):
    if get_admin_user(request) != None:
        adminUser = get_admin_user(request)
        certificates = Certificate.objects.all()
        context = {"adminUser": adminUser, "certificates": certificates}
        return render(request, "EducationAdmin/certificate.html", context)
    else:
        return redirect("adminLogin")
