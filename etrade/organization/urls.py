from django.urls import path,include
from . import views
urlpatterns = [
    path('<str:tin>',views.org,name='search')
]