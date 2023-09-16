from django.urls import path
from . import views
urlpatterns = [
    path('', views.index,name ="AdminIndex"),
    path('login', views.login,name ="adminLogin"),
    path('signout', views.adminSignout,name ="adminSignout"),
    path('upload', views.upload,name ="adminUpload"),
    path('universities', views.universities,name ="universites"),
        path('edit', views.universitiesEdit,name ="editUniversity"),
]
