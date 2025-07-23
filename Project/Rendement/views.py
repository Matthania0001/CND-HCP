from django.shortcuts import render
from django.views import View
from .forms import CompareSearchForm
from Collecte.forms import SearchForm
# Create your views here.
def rendement(request):
    return render(request, 'rendement.html')

class CompareRendView(View):
    template_name = 'comparRend.html'
    def get(self, request):
        form_compare = CompareSearchForm()
        formSearch = SearchForm(request.GET or None)
        return render(request, self.template_name, {'form_compare': form_compare,
                                                    'formSearch': formSearch})
    