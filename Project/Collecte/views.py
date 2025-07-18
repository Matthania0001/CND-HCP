from django.shortcuts import render

# Create your views here.
def collecte(request):
    return render(request, 'collecte.html')

from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection
from django.views import View
from .forms import PeriodiqueForm

from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection
from django.views import View
from .forms import PeriodiqueForm, MonographieForm, IndexeurForm, IndexationControlForm

class PeriodiqueAuthView(View):
    template_name = 'logins/periodique.html'
    form_class = PeriodiqueForm

    def get(self, request):
        form_periodique = self.form_class()
        return render(request, self.template_name, {'form_periodique': form_periodique})

    def post(self, request):
        form_periodique = self.form_class(request.POST)
        
        if form_periodique.is_valid():
            username = form_periodique.cleaned_data['username']
            password = form_periodique.cleaned_data['password']
            
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT 1 FROM admin WHERE login = %s AND pass = %s AND destination = 'collecte'",
                    [username, password]
                )
                if cursor.fetchone():
                    # Créer un token unique à chaque connexion
                    request.session['periodique_auth_token'] = f"token_{username}_{request.session.session_key}"
                    return redirect('periodique_protected')
                else:
                    messages.error(request, "Saisie incorrecte ou module non autorisé.")
        
        return render(request, self.template_name, {'form_periodique': form_periodique})


class PeriodiqueProtectedView(View):
    template_name = 'periodique.html'
    
    def dispatch(self, request, *args, **kwargs):
        # Vérification stricte + suppression immédiate de l'authentification
        if not request.session.get('periodique_auth_token'):
            return redirect('periodique_login')
        
        # Supprimer le token immédiatement après vérification
        token = request.session.pop('periodique_auth_token', None)
        if not token:
            return redirect('periodique_login')
            
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        return render(request, self.template_name)


def periodique_logout(request):
    request.session.flush()
    return redirect('periodiaque_login')


# Partie Monographie
class MonographieAuthView(View):
    template_name = 'logins/monographie.html'
    form_class = MonographieForm

    def get(self, request):
        form_monographie = self.form_class()
        return render(request, self.template_name, {'form_monographie': form_monographie})

    def post(self, request):
        form_monographie = self.form_class(request.POST)
        
        if form_monographie.is_valid():
            username = form_monographie.cleaned_data['username']
            password = form_monographie.cleaned_data['password']
            
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT 1 FROM admin WHERE login = %s AND pass = %s AND destination = 'collecte'",
                    [username, password]
                )
                if cursor.fetchone():
                    # Créer un token unique à chaque connexion
                    request.session['monographie_auth_token'] = f"token_{username}_{request.session.session_key}"
                    return redirect('monographie_protected')
                else:
                    messages.error(request, "Saisie incorrecte ou module non autorisé.")
        
        return render(request, self.template_name, {'form_monographie': form_monographie})


class MonographieProtectedView(View):
    template_name = 'monographie.html'
    
    def dispatch(self, request, *args, **kwargs):
        # Vérification stricte + suppression immédiate de l'authentification
        if not request.session.get('monographie_auth_token'):
            return redirect('monographie_login')
        
        # Supprimer le token immédiatement après vérification
        token = request.session.pop('monographie_auth_token', None)
        if not token:
            return redirect('monographie_login')
            
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        return render(request, self.template_name)


def monographie_logout(request):
    request.session.flush()
    return redirect('monographie_login')


# Partie Indexeur
class IndexeurAuthView(View):
    template_name = 'logins/indexeur.html'
    form_class = IndexeurForm

    def get(self, request):
        form_indexeur = self.form_class()
        return render(request, self.template_name, {'form_indexeur': form_indexeur})

    def post(self, request):
        form_indexeur = self.form_class(request.POST)
        
        if form_indexeur.is_valid():
            username = form_indexeur.cleaned_data['username']
            password = form_indexeur.cleaned_data['password']
            
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT 1 FROM admin WHERE login = %s AND pass = %s AND destination = 'suivi'",
                    [username, password]
                )
                if cursor.fetchone():
                    # Créer un token unique à chaque connexion
                    request.session['indexeur_auth_token'] = f"token_{username}_{request.session.session_key}"
                    return redirect('indexeur_protected')
                else:
                    messages.error(request, "Saisie incorrecte ou module non autorisé.")
        
        return render(request, self.template_name, {'form_indexeur': form_indexeur})


class IndexeurProtectedView(View):
    template_name = 'indexeur.html'
    
    def dispatch(self, request, *args, **kwargs):
        # Vérification stricte + suppression immédiate de l'authentification
        if not request.session.get('indexeur_auth_token'):
            return redirect('indexeur_login')
        
        # Supprimer le token immédiatement après vérification
        token = request.session.pop('indexeur_auth_token', None)
        if not token:
            return redirect('indexeur_login')
            
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        return render(request, self.template_name)


def indexeur_logout(request):
    request.session.flush()
    return redirect('indexeur_login')


# Partie Indexation et Controle
class IndexationControlAuthView(View):
    template_name = 'logins/indexationControl.html'
    form_class = IndexationControlForm

    def get(self, request):
        form_indexationControl = self.form_class()
        return render(request, self.template_name, {'form_indexationControl': form_indexationControl})

    def post(self, request):
        form_indexationControl = self.form_class(request.POST)
        
        if form_indexationControl.is_valid():
            username = form_indexationControl.cleaned_data['username']
            password = form_indexationControl.cleaned_data['password']
            
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT 1 FROM admin WHERE login = %s AND pass = %s AND destination = 'suivi'",
                    [username, password]
                )
                if cursor.fetchone():
                    # Créer un token unique à chaque connexion
                    request.session['indexationControl_auth_token'] = f"token_{username}_{request.session.session_key}"
                    return redirect('indexationControl_protected')
                else:
                    messages.error(request, "Saisie incorrecte ou module non autorisé.")
        
        return render(request, self.template_name, {'form_indexationControl': form_indexationControl})


class IndexationControlProtectedView(View):
    template_name = 'indexationControl.html'
    
    def dispatch(self, request, *args, **kwargs):
        # Vérification stricte + suppression immédiate de l'authentification
        if not request.session.get('indexationControl_auth_token'):
            return redirect('indexationControl_login')
        
        # Supprimer le token immédiatement après vérification
        token = request.session.pop('indexationControl_auth_token', None)
        if not token:
            return redirect('indexationControl_login')
            
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        return render(request, self.template_name)


def indexationControl_logout(request):
    request.session.flush()
    return redirect('indexationControl_login')