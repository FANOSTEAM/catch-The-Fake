import io

import qrcode
from django.core.exceptions import ObjectDoesNotExist
from django.http import FileResponse, HttpResponseNotFound, JsonResponse
from django.shortcuts import redirect, render
from EducationAdmin.models import Collage, Major, Title, University
from reportlab.lib import utils
from reportlab.lib.colors import black, magenta, red
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, mm
from reportlab.pdfgen import canvas
from Student.models import Certificate

from CTF.settings import SECRET_KEY
from CTF.views import get_employer_from_session

# from cryptography.fernet import Fernet
key = b"h-rU6ELYpVCgBMr_oA8Yjw7yTtl1pBwW6zF3VSGDzxE="


def certificate_generator(certificate_obj,mode=1):
    buffer = io.BytesIO()

    profile = utils.ImageReader(certificate_obj.profile_picture.path)
    logo = utils.ImageReader(certificate_obj.title.major.collage.university.logo.path)
    img_width, img_height = profile.getSize()
    width_logo, height_logo = logo.getSize()
    my_canvas = canvas.Canvas(buffer, pagesize=A4)
    my_canvas.saveState()
    my_canvas.setFillColorRGB(0, 0, 0.77)
    my_canvas.setSubject(
        "Cetified to" + certificate_obj.firstName + " " + certificate_obj.middleName
    )
    my_canvas.drawImage(
        certificate_obj.title.major.collage.university.logo.path,
        ((210 * mm)) - 2.5 * inch,
        (297 * mm) - (1.5 * inch),
        width=2 * inch,
        height=1.5 * inch,
        mask="auto",
    )
    my_canvas.drawImage(
        certificate_obj.profile_picture.path,
        10,
        (297 * mm) - (1.5 * inch),
        width=2 * inch,
        height=1.5 * inch,
    )
    my_canvas.setFont("Times-Roman", size=28)
    qr = qrcode.QRCode(version=1, box_size=10, border=5)

    # Adding data to the instance 'qr'
    qr.add_data(str(certificate_obj.id).encode())
    print(str(certificate_obj.id).encode())
    qr.make(fit=True)
    img = qr.make_image(fill_color="red", back_color="white")
    img.save("qr.png")
    ir = utils.ImageReader("qr.png")
    my_canvas.drawImage("qr.png", 0, 0, width=2 * inch, preserveAspectRatio=True)

    my_canvas.setLineWidth(1)
    my_canvas.setFillColor(red)
    if len(certificate_obj.title.major.collage.university.name) <= 21:
        my_canvas.drawString(
            ((180 * mm)) / 2 - 100,
            9.3 * inch,
            certificate_obj.title.major.collage.university.name,
        )
    else:
        my_canvas.setFont("Times-Roman", size=15)
        my_canvas.drawString(
            ((180 * mm)) / 2 - 100,
            9.3 * inch,
            certificate_obj.title.major.collage.university.name,
        )
    my_canvas.drawString(100, 8.3 * inch, certificate_obj.type_of_certificate)
    my_canvas.setLineWidth(2.5)

    my_canvas.setFont("Times-Roman", size=12)
    my_canvas.setLineWidth(1.3)
    my_canvas.setFillColor(black)
    my_canvas.drawString(
        (((180 * mm) / 2) - (width_logo / 2)), 7.8 * inch, "This is to certify that"
    )
    my_canvas.drawCentredString(
        ((180 * mm) - (width_logo / 2)) / 2,
        7.2 * inch,
        certificate_obj.firstName
        + " "
        + certificate_obj.middleName
        + " "
        + certificate_obj.lastName,
    )
    my_canvas.drawCentredString(
        ((180 * mm) - (width_logo / 2)) / 2, 6.5 * inch, "graduated from school of "
    )
    my_canvas.drawCentredString(
        ((200 * mm) - (width_logo / 2)) / 2, 6 * inch, certificate_obj.school.name
    )
    my_canvas.drawCentredString(
        ((180 * mm) - (width_logo / 2)) / 2,
        5.5 * inch,
        f"with {certificate_obj.title.title} in",
    )
    my_canvas.drawCentredString(
        ((180 * mm) - (width_logo / 2)) / 2, 5 * inch, certificate_obj.title.major.name
    )
    my_canvas.drawCentredString(
        ((180 * mm) - (width_logo / 2)) / 2,
        4.5 * inch,
        f"(Major GPA of {certificate_obj.GPA} and CGPA of {certificate_obj.CGPA})",
    )
    my_canvas.drawCentredString(
        ((180 * mm) - (width_logo / 2)) / 2, 4 * inch, f"ON {certificate_obj.issued_on}"
    )
    my_canvas.setAuthor("ethiopian minister of education")
    my_canvas.setTitle(str(certificate_obj.title.title) + "Certificate")
    my_canvas.save()
    buffer.seek(0)
    if mode==2:
        return buffer
    return FileResponse(buffer, as_attachment=False, filename="certificate.pdf")


def index(request):
    if get_employer_from_session(request):
        user = get_employer_from_session(request)
        universities_objs = University.objects.all()
        print(universities_objs)
        context = {"user": user, "universities": universities_objs}
        return render(request, "verifier/index.html", context)
    else:
        return redirect("login")


def search(request):
    if get_employer_from_session(request) != None:
        if request.method == "GET":
            req = request.GET
            try:
                certificate = Certificate.objects.get(id=req["id"])
                return certificate_generator(certificate)
            except Certificate.DoesNotExist:
                return JsonResponse({"not found": True})
        elif request.method == "POST":
            if "search1" in request.POST:
                university = request.POST["university"]
                try:
                    un = University.objects.get(id=int(university))
                    collages = un.collage_set.all()
                except University.DoesNotExist:
                    return HttpResponseNotFound()
                context = {"collages": collages}
                return render(request, "verifier/search1.html", context)

            elif "search2" in request.POST:
                collage_id = request.POST["collage"]
                collage = Collage.objects.get(id=int(collage_id))
                majors = collage.major_set.all()
                context = {"majors": majors}
                return render(request, "verifier/search1.html", context)
            elif "search3" in request.POST:
                major_id = request.POST["major"]
                major = Major.objects.get(id=int(major_id))
                titles = major.title_set.all()
                context = {"titles": titles}
                return render(request, "verifier/search1.html", context)
            elif "search4" in request.POST:
                title_id = request.POST["title"]
                first_name = request.POST["firstName"]
                second_name = request.POST["MiddleName"]
                last_name = request.POST["LastName"]
                date = request.POST["date"]
                gpa = request.POST["gpa"]
                CGPA = request.POST["CGPA"]
                title = Title.objects.get(id=int(title_id))
                try:
                    certificate = Certificate.objects.get(
                        firstName=first_name,
                        middleName=second_name,
                        lastName=last_name,
                        issued_on=date,
                        GPA=gpa,
                        CGPA=CGPA,
                        title=title,
                    )
                    print("yes")
                except Exception:
                    print("Nooooooo")
                    return JsonResponse({"not found": True})

                return certificate_generator(certificate)

    else:
        return redirect("login")
