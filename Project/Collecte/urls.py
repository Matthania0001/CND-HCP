from django.urls import path
from . import views
urlpatterns = [
    path('', views.collecte, name='collecte'),
    path('periodique/login/', views.PeriodiqueAuthView.as_view(), name='periodique_login'),
    path('periodique/protected/', views.PeriodiqueProtectedView.as_view(), name='periodique_protected'),
    path('periodique/logout/', views.periodique_logout, name='periodique_logout'),
]
