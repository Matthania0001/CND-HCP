from django.urls import path
from . import views
urlpatterns = [
    path('', views.ArchivageDocView.as_view(), name='archivage'),

]