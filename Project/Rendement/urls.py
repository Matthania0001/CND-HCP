from django.urls import path
from . import views
urlpatterns = [
    path('', views.rendement, name='rendement'),
    path('comparaison/', views.CompareRendView.as_view(), name='CompareRendement'),   
    
]

