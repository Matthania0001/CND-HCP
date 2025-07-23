from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection
from django.views import View
from .forms import SourceLoginForm, DomaineLoginForm, SourceSuppressionForm, SourceAjoutForm, DomaineSuppressionForm, DomaineAjoutForm
from Collecte.forms import SearchForm
from django.db import connection
# Create your views here.
def gestion(request):
    return render(request, 'gestion.html')

class SourceAuthView(View):
    template_name = 'logins/source.html'
    form_class = SourceLoginForm

    def get(self, request):
        form_source = self.form_class()
        return render(request, self.template_name, {'form_source': form_source})

    def post(self, request):
        form_source = self.form_class(request.POST)
        
        if form_source.is_valid():
            username = form_source.cleaned_data['username']
            password = form_source.cleaned_data['password']
            
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT 1 FROM admin WHERE login = %s AND pass = %s AND destination = 'ajout_supp'",
                    [username, password]
                )
                if cursor.fetchone():
                    # Créer un token unique à chaque connexion
                    request.session['source_auth_token'] = f"token_{username}_{request.session.session_key}"
                    return redirect('source_protected')
                else:
                    messages.error(request, "Saisie incorrecte ou module non autorisé.")
        
        return render(request, self.template_name, {'form_source': form_source})

class SourceProtectedView(View):
    template_name = 'source.html'

    def dispatch(self, request, *args, **kwargs):
        # Vérification stricte + suppression du token
        if not request.session.get('source_auth_token'):
            return redirect('source_login')

        token = request.session.pop('source_auth_token', None)
        if not token:
            return redirect('source_login')

        return super().dispatch(request, *args, **kwargs)
    def post(self, request):
        source_form_sup = SourceSuppressionForm(request.POST)
        source_form_ajt = SourceAjoutForm(request.POST)
        if source_form_sup.is_valid():
            source = source_form_sup.cleaned_data['source']
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM source WHERE source = %s", [source])
            messages.success(request, f"Source {source} supprimée avec succès.")
            return redirect('source_protected')
        if source_form_ajt.is_valid():
            nom_source = source_form_ajt.cleaned_data['nom_source']
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO source (source) VALUES (%s)", [nom_source])
            messages.success(request, f"Source {nom_source} ajoutée avec succès.")
            return redirect('source_protected')
        context =  {
            'source_form_sup': source_form_sup,
            'source_form_ajt': source_form_ajt,
        }
        return render(request, self.template_name, context)
    def get(self, request):
        formSearch = SearchForm(request.GET or None)
        source_form_sup = SourceSuppressionForm(request.POST)
        source_form_ajt = SourceAjoutForm(request.POST)
        context =  {
            'source_form_sup': source_form_sup,
            'source_form_ajt': source_form_ajt,
            'formSearch': formSearch
        }
        return render(request, self.template_name, context)
    


class DomaineAuthView(View):
    template_name = 'logins/domaine.html'
    form_class = DomaineLoginForm

    def get(self, request):
        form_domaine = self.form_class()
        return render(request, self.template_name, {'form_domaine': form_domaine})

    def post(self, request):
        form_domaine = self.form_class(request.POST)
        
        if form_domaine.is_valid():
            username = form_domaine.cleaned_data['username']
            password = form_domaine.cleaned_data['password']
            
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT 1 FROM admin WHERE login = %s AND pass = %s AND destination = 'ajout_supp'",
                    [username, password]
                )
                if cursor.fetchone():
                    # Créer un token unique à chaque connexion
                    request.session['domaine_auth_token'] = f"token_{username}_{request.session.session_key}"
                    return redirect('domaine_protected')
                else:
                    messages.error(request, "Saisie incorrecte ou module non autorisé.")
        
        return render(request, self.template_name, {'form_domaine': form_domaine})

class DomaineProtectedView(View):
    template_name = 'domaine.html'

    def dispatch(self, request, *args, **kwargs):
        # Vérification stricte + suppression du token
        if not request.session.get('domaine_auth_token'):
            return redirect('domaine_login')

        token = request.session.pop('domaine_auth_token', None)
        if not token:
            return redirect('domaine_login')

        return super().dispatch(request, *args, **kwargs)
    def post(self, request):
        domaine_form_sup = DomaineSuppressionForm(request.POST)
        domaine_form_ajt = DomaineAjoutForm(request.POST)
        if domaine_form_sup.is_valid():
            domaine = domaine_form_sup.cleaned_data['source']
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM domaine WHERE domaine = %s", [domaine])
            messages.success(request, f"Domaine {domaine} supprimé avec succès.")
            return redirect('domaine_protected')
        if domaine_form_ajt.is_valid():
            nom_source = domaine_form_ajt.cleaned_data['nom_source']
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO domaine (domaine) VALUES (%s)", [nom_source])
            messages.success(request, f"Source {nom_source} ajoutée avec succès.")
            return redirect('domaine_protected')
        context =  {
            'domaine_form_sup': domaine_form_sup,
            'domaine_form_ajt': domaine_form_ajt,
        }
        return render(request, self.template_name, context)
    def get(self, request):
        formSearch = SearchForm(request.GET or None)
        domaine_form_sup = DomaineSuppressionForm(request.POST)
        domaine_form_ajt = DomaineAjoutForm(request.POST)
        context =  {
            'domaine_form_sup': domaine_form_sup,
            'domaine_form_ajt': domaine_form_ajt,
            'formSearch': formSearch
        }
        return render(request, self.template_name, context)
    