import zipfile
from io import BytesIO

from django.http import HttpResponse
from django.shortcuts import redirect, render
from EducationAdmin.models import Collage, Major, Title, University
from Student.models import Certificate
from verifier.views import certificate_generator


def generate_zip(list_of_tuples):
    """function to write zip file"""
    mem_zip = BytesIO()
    with zipfile.ZipFile(mem_zip, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        for f in list_of_tuples:
            zf.writestr(f[0], f[1].read())
    return mem_zip.getvalue()


def get_registrar(request):
    if request.session.has_key("regedit"):
        try:
            username = request.session["regedit"]
            password = request.session["password"]

            user = University.objects.get(
                user_name=username,
                password=password,
            )
            return user
        except Exception:
            return None
    else:
        return None


def university_login(request):
    """a view where university registrars can login so that they can download certificates"""
    if get_registrar(request) is not None:
        return redirect("university_index")
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        remember = request.POST["remember"]
        try:
            admin = University.objects.get(user_name=username, password=password)
            request.session["regedit"] = username
            request.session["password"] = password
            print(remember)
            if remember == "true":
                pass
            else:
                request.session.set_expiry(0)
            request.session.modified = True
            return redirect("university_index")
        except Exception:
            context = {"err": True}
            return render(request, "universityLogin.html", context)

    return render(request, "universityLogin.html", {})


def university_index(request):
    if get_registrar(request) is not None:
        registrar = get_registrar(request)
        collages = registrar.collage_set.all()
        if "search2" in request.POST:
            collage_id = request.POST["collage"]
            collage = Collage.objects.get(id=int(collage_id))
            majors = collage.major_set.all()
            context = {"majors": majors}
            return render(request, "verifier/search2.html", context)
        elif "search3" in request.POST:
            major_id = request.POST["major"]
            major = Major.objects.get(id=int(major_id))
            titles = major.title_set.all()
            context = {"titles": titles}
            return render(request, "verifier/search2.html", context)
        elif "search4i" in request.POST:
            title_id = request.POST["title"]

            date = request.POST["date"]

            title = Title.objects.get(id=int(title_id))
            if date == "2000-09-29":
                certificates = Certificate.objects.filter(
                    title=title,
                )
            else:
                certificates = Certificate.objects.filter(
                    issued_on=date,
                    title=title,
                )
            certificate_tuple = []

            count = 0
            for i in certificates:
                certificate_tuple.append(
                    (
                        i.firstName + str(count) + str(i.issued_on) + ".pdf",
                        certificate_generator(i, mode=2),
                    )
                )
                count += 1
            full_zip_in_memory = generate_zip(certificate_tuple)
            response = HttpResponse(
                full_zip_in_memory, content_type="application/force-download"
            )
            response["Content-Disposition"] = 'attachment; filename="{}"'.format(
                "DegreeCertificate.zip"
            )
            return response

        return render(
            request, "University_index.html", {"reg": registrar, "collages": collages}
        )
    return redirect("ulogin")
