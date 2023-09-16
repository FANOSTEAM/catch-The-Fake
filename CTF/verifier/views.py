from django.shortcuts import render,redirect
from Student.models import Certificate
from django.core.exceptions import ObjectDoesNotExist
from reportlab.lib import utils
from reportlab.lib.pagesizes import A4
from reportlab.lib.units  import inch , mm
from reportlab.pdfgen import canvas
import io
from CTF.settings import SECRET_KEY
from django.http import FileResponse
from reportlab.lib.colors import magenta, red,black
import qrcode
from CTF.views import get_employer_from_session

# from cryptography.fernet import Fernet
key =b'h-rU6ELYpVCgBMr_oA8Yjw7yTtl1pBwW6zF3VSGDzxE='
def certificate_generator(certificate_obj):
    buffer = io.BytesIO()

    profile = utils.ImageReader(certificate_obj.profile_picture.path)
    logo=utils.ImageReader(certificate_obj.title.major.collage.university.logo.path)
    img_width, img_height = profile.getSize()
    width_logo,height_logo= logo.getSize()
    my_canvas = canvas.Canvas(buffer,
                              pagesize=A4)
    my_canvas.saveState()
    my_canvas.setFillColorRGB(0,0,0.77)
    my_canvas.setSubject("Cetified to"+certificate_obj.firstName+" "+certificate_obj.middleName)
    my_canvas.drawImage(certificate_obj.title.major.collage.university.logo.path, ((210*mm))/2,250*mm,
                        height=100, preserveAspectRatio=True, mask='auto')
    my_canvas.drawImage(certificate_obj.profile_picture.path, 0, 210*mm,
                       width=2*inch,preserveAspectRatio=True)
    my_canvas.setFont("Times-Roman",size=28)
    qr = qrcode.QRCode(version = 1,
                   box_size = 10,
                   border = 5)
 
# Adding data to the instance 'qr'
    qr.add_data(str(certificate_obj.id).encode())
    print(str(certificate_obj.id).encode())
    qr.make(fit = True)
    img = qr.make_image(fill_color = 'red',
                    back_color = 'white')
    img.save('qr.png')
    ir= utils.ImageReader('qr.png')
    my_canvas.drawImage('qr.png',0, 0,
                       width=2*inch,preserveAspectRatio=True)

    
    my_canvas.setLineWidth(1) 
    my_canvas.setFillColor(red)
    my_canvas.drawString( ((100*mm))/2-100,9.3*inch,certificate_obj.title.major.collage.university.name)
    my_canvas.drawString( 150,8.3*inch,certificate_obj.type_of_certificate)
    my_canvas.setLineWidth(2.5)
   
    my_canvas.setFont("Times-Roman",size=18)
    my_canvas.setLineWidth(1)
    my_canvas.setFillColor(black)
    my_canvas.drawString( ((210*mm)-(width_logo/2))/2,7.8*inch,"This is to certify that")
    my_canvas.drawCentredString( ((270*mm)-(width_logo/2))/2,7.2*inch,certificate_obj.firstName +" "+ certificate_obj.middleName+" "+certificate_obj.lastName)
    my_canvas.drawCentredString( ((270*mm)-(width_logo/2))/2,6.5*inch,"graduated from school of ")
    my_canvas.drawCentredString( ((270*mm)-(width_logo/2))/2,6*inch,certificate_obj.school.name)
    my_canvas.drawCentredString( ((270*mm)-(width_logo/2))/2,5.5*inch,f"with {certificate_obj.title.title} in")
    my_canvas.drawCentredString( ((270*mm)-(width_logo/2))/2,5*inch,certificate_obj.title.major.name)
    my_canvas.drawCentredString( ((270*mm)-(width_logo/2))/2,4.5*inch,f'(Major GPA of {certificate_obj.GPA} and CGPA of {certificate_obj.CGPA})')
    my_canvas.drawCentredString( ((270*mm)-(width_logo/2))/2,4*inch,f'ON {certificate_obj.issued_on}')
    my_canvas.setAuthor("ethiopian minister of education")
    my_canvas.setTitle(str(certificate_obj.title.title)+"Certificate")
    my_canvas.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=False, filename="certificate.pdf")
def index(request):
    if get_employer_from_session(request):
        user=get_employer_from_session(request)
        context={'user':user}
        return render(request, "verifier/index.html",context)
    else:
        return redirect('login')
def search(request):
    if get_employer_from_session(request)!=None:
        if request.method=='GET':
            req=request.GET
            try:
                certificate=Certificate.objects.get(id=req['id'])
                return certificate_generator(certificate)
            except Certificate.DoesNotExist:
                return "hi"
        elif request.method=='POST':
            if 'search1' in request.POST:
                university=request.POST['university']
                
            elif 'search2' in request.POST:
                pass 
    else:
        return redirect('login')