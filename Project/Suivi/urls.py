from django.urls import path
from . import views
urlpatterns = [
    path('', views.suivi, name='suivi'),
    
    #Indexeur URLs
    path('indexeur/login/', views.IndexeurAuthView.as_view(), name='indexeur_login'),
    path('indexeur/protected/', views.IndexeurProtectedView.as_view(), name='indexeur_protected'),
    path('indexeur/logout/', views.indexeur_logout, name='indexeur_logout'),

    #Indexation et Controle URLs
    path('indexationControl/login/', views.IndexationControlAuthView.as_view(), name='indexationControl_login'),
    path('indexationControl/protected/', views.IndexationControlProtectedView.as_view(), name='indexationControl_protected'),
    path('indexationControl/logout/', views.indexationControl_logout, name='indexationControl_logout'),
    #Prise de Vue URLs
    path('priseVue/login/', views.PriseVueAuthView.as_view(), name='priseVue_login'),
    path('priseVue/protected/', views.PriseVueProtectedView.as_view(), name='priseVue_protected'),
    path('priseVue/logout/', views.priseVue_logout, name='priseVue_logout'),
   
]

