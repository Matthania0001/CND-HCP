from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection
from django.views import View
from .forms import SourceLoginForm, DomaineLoginForm
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
