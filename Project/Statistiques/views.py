from django.shortcuts import render
from .forms import DocTypeSearchForm
from Collecte.forms import SearchForm
from django.views import View
from django.db import connection
# Create your views here.
def statistiques(request):
    return render(request, 'statistiques.html')
class DocTypeSearchView(View):
    template_name = 'listeDocType.html'
    def get(self, request):
        form_search_doc_type = DocTypeSearchForm()
        formSearch = SearchForm(request.GET or None)
        return render(request, self.template_name, {'form_search_doc_type': form_search_doc_type,
                                                    'formSearch': formSearch})
    
class StatistiquesView(View):
    template_name = 'affichageStat.html'
    def get(self, request):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT type_support, COUNT(*) 
                FROM doc
                GROUP BY type_support
            """)
            resultForSupport = cursor.fetchall()
            statsBySupport = {row[0]: row[1] for row in resultForSupport}
            cursor.execute("""
                SELECT f.source, COUNT(d.n_enregistrement)
                FROM doc d
                INNER JOIN fournit f ON d.n_enregistrement = f.n_enregistrement
                GROUP BY f.source
            """)
                
            resultForSource = cursor.fetchall()
            statsBySource = {row[0]: row[1] for row in resultForSource}
            cursor.execute("""
                SELECT domaine, COUNT(*) 
                FROM doc
                GROUP BY domaine
            """)
            resultForDomaine = cursor.fetchall()
            statsByDomaine = {row[0]: row[1] for row in resultForDomaine}

            cursor.execute("""
                SELECT periodicite, COUNT(*) 
                FROM doc
                GROUP BY periodicite
            """)
            resultForPeriodicite = cursor.fetchall()
            statsByPeriodicite = {row[0]: row[1] for row in resultForPeriodicite}

            cursor.execute("""
                SELECT lang, COUNT(*) 
                FROM doc
                GROUP BY lang
            """)
            resultForLangue = cursor.fetchall()
            statsByLangue = {row[0]: row[1] for row in resultForLangue}
            cursor.execute("""
                SELECT f.obligation, COUNT(d.n_enregistrement)
                FROM doc d
                INNER JOIN fournit f ON d.n_enregistrement = f.n_enregistrement
                GROUP BY f.obligation
            """)
                
            resultForAcquisition = cursor.fetchall()
            statsByAcquisition = {row[0]: row[1] for row in resultForAcquisition}
            cursor.execute("""
                
            """)
            resultForArchive = cursor.fetchall()
            statsByArchive = {row[0]: row[1] for row in resultForArchive}
        return render(request, self.template_name, {'statsBySupport': statsBySupport,
                                                    'statsBySource': statsBySource,
                                                    'statsByDomaine': statsByDomaine,
                                                    'statsByPeriodicite': statsByPeriodicite,
                                                    'statsByLangue': statsByLangue,
                                                    'statsByAcquisition': statsByAcquisition,
                                                    })