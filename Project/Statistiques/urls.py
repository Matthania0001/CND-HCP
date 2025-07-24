from django.urls import path
from . import views
urlpatterns = [
    path('', views.statistiques, name='statistiques'),
    path('listeDoc/', views.DocTypeSearchView.as_view(), name = 'listeDocType')
   
]

