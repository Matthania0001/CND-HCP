from django.urls import path
from . import views
urlpatterns = [
    path('', views.collecte, name='collecte'),
    #Collecte Login URLs
    path('login/', views.CollectAuthView.as_view(), name='collecte_login'),
    path('protected/', views.CollectDocView.as_view(), name='collect_protected'),
    path('periodique/login/', views.PeriodiqueAuthView.as_view(), name='periodique_login'),
    path('periodique/protected/', views.PeriodiqueProtectedView.as_view(), name='periodique_protected'),
    path('periodique/logout/', views.periodique_logout, name='periodique_logout'),
    #Monographie URLs
    path('monographie/login/', views.MonographieAuthView.as_view(), name='monographie_login'),
    path('monographie/protected/', views.MonographieProtectedView.as_view(), name='monographie_protected'),
    path('monographie/logout/', views.monographie_logout, name='monographie_logout'),
    #Indexeur URLs
    path('resultats/', views.resultatSearch, name='resultats'),
    #Partie enregistrement d'un periodique
   
]

