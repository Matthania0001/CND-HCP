from django.urls import path
from . import views
urlpatterns = [
    path('', views.gestion, name='gestion'),
    path('source/', views.SourceAuthView.as_view(), name = 'source_login'),
    path('domaine/', views.DomaineAuthView.as_view(), name = 'domaine_login'),
    path('source/protected/', views.SourceProtectedView.as_view(), name='source_protected'),
    path('domaine/protected/', views.DomaineProtectedView.as_view(), name='domaine_protected'),
    path('bynumber/', views.SearchByNumberView.as_view(), name='bynumber'),
   
]

