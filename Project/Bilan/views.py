from django.shortcuts import render
from django.views import View
from .forms import DocumentSearchForm, EtsSearchForm
from Collecte.forms import SearchForm
# Create your views here.
def bilan(request):
    return render(request, 'bilan.html')

class DocumentSearchView(View):
    template_name = 'list_doc.html'
    def get(self, request):
        form_search_doc = DocumentSearchForm()
        formSearch = SearchForm(request.GET or None)
        return render(request, self.template_name, {'form_search_doc': form_search_doc,
                                                    'formSearch': formSearch})
        
        
class EtsSearchView(View):
    template_name = 'list_etb.html'
    def get(self, request):
        form_search_ets = EtsSearchForm()
        formSearch = SearchForm(request.GET or None)
        return render(request, self.template_name, {'form_search_ets': form_search_ets,
                                                    'formSearch': formSearch})
    