from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="AdminIndex"),
    path("login", views.login, name="adminLogin"),
    path("signout", views.adminSignout, name="adminSignout"),
    path("certificates", views.certificates, name="certificates"),
    path("upload", views.upload, name="adminUpload"),
    path("universities", views.universities, name="universites"),
    path("edit/university", views.universitiesEdit, name="editUniversity"),
    path("collage/<int:collage_id>", views.collage, name="collages"),
    path("major/<int:collage_id>", views.major, name="majors"),
    path("degree/<int:major_id>", views.degree, name="degree"),
    path("edit/major", views.major_edit, name="editMajor"),
    path("edit/degree", views.degree_edit, name="degreeEdit"),
    path("edit/collage", views.collage_edit, name="editCollage"),
]
