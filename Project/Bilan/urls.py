from django.urls import path
from . import views
urlpatterns = [
    path('', views.bilan, name='bilan'),   
]

