from django.urls import path
from . import views
urlpatterns = [
    path('', views.bilan, name='bilan'),   
    path('listeDoc/', views.DocumentSearchView.as_view(), name = 'listeDoc'),
    path('listeEts/', views.EtsSearchView.as_view(), name = 'listeEts')
]

