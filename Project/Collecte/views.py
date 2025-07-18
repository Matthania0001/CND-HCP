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
from .forms import PeriodiqueForm

class PeriodiqueAuthView(View):
    template_name = 'logins/periodique.html'
    form_class = PeriodiqueForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
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
        
        return render(request, self.template_name, {'form': form})


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
    return redirect('periodique_login')