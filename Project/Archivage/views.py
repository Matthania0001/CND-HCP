from django.shortcuts import render
from django.views import View
from django.db import connection
from .forms import ArchivageDocForm
from Collecte.forms import SearchForm
# Create your views here.



class ArchivageDocView(View):
    template_name = 'archivage.html'
    def get(self, request):
        form_archivage_doc = ArchivageDocForm()
        formSearch = SearchForm(request.GET or None)
        return render(request, self.template_name, {'form_archivage_doc': form_archivage_doc,
                                                    'formSearch': formSearch})