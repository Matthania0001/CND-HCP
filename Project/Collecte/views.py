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
from .forms import PeriodiqueForm, MonographieForm, IndexeurForm, IndexationControlForm, PriseVueForm, SearchForm

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

from django.views.generic.base import TemplateView
# class PeriodiqueProtectedView(View):
#     template_name = 'periodique.html'
#     def dispatch(self, request, *args, **kwargs):
#         # Vérification stricte + suppression immédiate de l'authentification
#         if not request.session.get('periodique_auth_token'):
#             return redirect('periodique_login')
        
#         # Supprimer le token immédiatement après vérification
#         token = request.session.pop('periodique_auth_token', None)
#         if not token:
#             return redirect('periodique_login')
            
#         return super().dispatch(request, *args, **kwargs)
#     def get(self, request):
#         formSearch = SearchForm(request.GET or None)
#         return render(request, self.template_name, {'formSearch': formSearch})

from django.shortcuts import render, redirect
from django.views import View
from .forms import SearchForm

# class PeriodiqueProtectedView(View):
#     template_name = 'periodique.html'

#     def dispatch(self, request, *args, **kwargs):
#         # Vérification stricte + suppression du token
#         if not request.session.get('periodique_auth_token'):
#             return redirect('periodique_login')

#         token = request.session.pop('periodique_auth_token', None)
#         if not token:
#             return redirect('periodique_login')

#         return super().dispatch(request, *args, **kwargs)

#     def get(self, request):
#         # Initialisation du formulaire avec GET existant (auto remplit)
#         formSearch = SearchForm(request.GET or None)
#         return render(request, self.template_name, {'formSearch': formSearch})

from django.shortcuts import render, redirect
from django.views import View
from .forms import ArticlePeriodiqueForm, SearchForm
from django.contrib import messages
from Main.models import Doc, Ecriture, Edition, Fournit, Collecte, Suivi

class PeriodiqueProtectedView(View):
    template_name = 'periodique.html'

    def dispatch(self, request, *args, **kwargs):
        # Vérification stricte + suppression du token
        if not request.session.get('periodique_auth_token'):
            return redirect('periodique_login')

        token = request.session.pop('periodique_auth_token', None)
        if not token:
            return redirect('periodique_login')

        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        # Initialisation des formulaires
        formSearch = SearchForm(request.GET or None)
        article_form = ArticlePeriodiqueForm()
        
        context = {
            'formSearch': formSearch,
            'article_form': article_form,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        article_form = ArticlePeriodiqueForm(request.POST)
        formSearch = SearchForm(request.GET or None)
        
        if article_form.is_valid():
            try:
                # Sauvegarde dans la table Doc
                doc = Doc.objects.create(
                    n_enregistrement=article_form.cleaned_data['n_enregistrement'],
                    titre=article_form.cleaned_data['titre'],
                    titre_article=article_form.cleaned_data['titre_article'],
                    periodicite='p',  # Périodique
                    vol=article_form.cleaned_data['vol'],
                    tom=article_form.cleaned_data['tom'],
                    num=article_form.cleaned_data['num'],
                    pages=article_form.cleaned_data['pages'],
                    domaine=article_form.cleaned_data['domaine'].domaine,
                    statut='collecte',
                    lang=article_form.cleaned_data['langue'],
                )
                
                # Gestion des auteurs (séparés par /)
                auteurs = article_form.cleaned_data['auteurs'].split('/')
                for auteur in auteurs:
                    if auteur.strip():  # Ignore les chaînes vides
                        Ecriture.objects.create(
                            auteur=auteur.strip(),
                            n_enregistrement=doc.n_enregistrement
                        )
                
                # Sauvegarde dans Edition
                if article_form.cleaned_data['editeur']:
                    Edition.objects.create(
                        editeur=article_form.cleaned_data['editeur'].editeur,
                        n_enregistrement=doc.n_enregistrement,
                    )
                
                # Sauvegarde dans Fournit
                Fournit.objects.create(
                    source=article_form.cleaned_data['source_expeditrice'].source,
                    n_enregistrement=doc.n_enregistrement,
                    date_reception=article_form.cleaned_data['date_reception'],
                    obligation=article_form.cleaned_data['type_acquisition']
                )
                
                # Sauvegarde dans Collecte
                Collecte.objects.create(
                    nomrc=article_form.cleaned_data['responsable_saisie'],
                    n_enregistrement=doc.n_enregistrement,
                    datsaisi_c=article_form.cleaned_data['date_saisie']
                )
                
                # Sauvegarde dans Suivi
                Suivi.objects.create(
                    noms=article_form.cleaned_data['responsable_saisie'],
                    n_enregistrement=doc.n_enregistrement,
                    datenvoi_t=article_form.cleaned_data['date_envoi']
                )
                
                messages.success(request, "L'article périodique a été enregistré avec succès!")
                return redirect('periodique')
            
            except Exception as e:
                messages.error(request, f"Une erreur est survenue: {str(e)}")
        
        # Si le formulaire n'est pas valide ou erreur d'enregistrement
        context = {
            'formSearch': formSearch,
            'article_form': article_form,
        }
        return render(request, self.template_name, context)



def periodique_logout(request):
    request.session.flush()
    return redirect('periodique_login')


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
                    "SELECT 1 FROM admin WHERE login = %s AND pass = %s AND destination = 'indexation'",
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


# Partie Prise de Vue
class PriseVueAuthView(View):
    template_name = 'logins/priseVue.html'
    form_class = PriseVueForm

    def get(self, request):
        form_priseVue = self.form_class()
        return render(request, self.template_name, {'form_priseVue': form_priseVue})

    def post(self, request):
        form_priseVue = self.form_class(request.POST)
        
        if form_priseVue.is_valid():
            username = form_priseVue.cleaned_data['username']
            password = form_priseVue.cleaned_data['password']
            
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT 1 FROM admin WHERE login = %s AND pass = %s AND destination = 'vue'",
                    [username, password]
                )
                if cursor.fetchone():
                    # Créer un token unique à chaque connexion
                    request.session['priseVue_auth_token'] = f"token_{username}_{request.session.session_key}"
                    return redirect('priseVue_protected')
                else:
                    messages.error(request, "Saisie incorrecte ou module non autorisé.")
        
        return render(request, self.template_name, {'form_priseVue': form_priseVue})


class PriseVueProtectedView(View):
    template_name = 'priseVue.html'
    
    def dispatch(self, request, *args, **kwargs):
        # Vérification stricte + suppression immédiate de l'authentification
        if not request.session.get('priseVue_auth_token'):
            return redirect('priseVue_login')
        
        # Supprimer le token immédiatement après vérification
        token = request.session.pop('priseVue_auth_token', None)
        if not token:
            return redirect('priseVue_login')
            
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        return render(request, self.template_name)


def priseVue_logout(request):
    request.session.flush()
    return redirect('priseVue_login')




from django.shortcuts import render, redirect
from .forms import SearchForm

from django.shortcuts import render
from django.db.models import Q
from Main.models import Doc, Fournit, Edition, Ecriture  # Importez vos modèles existants

from django.shortcuts import render
from django.db import connection

# def resultatSearch(request):
#     if request.method == 'GET' and 'titre' in request.GET:
#         terme_recherche = request.GET['titre'].strip()
#         termes = terme_recherche.lower().split()
        
#         # Construction de la partie WHERE avec tous les termes
#         where_parts = []
#         params = []
#         for terme in termes:
#             where_parts.append("((LOWER(d.titre) LIKE %s) OR (LOWER(d.titre_article) LIKE %s))")
#             params.extend([f"%{terme}%", f"%{terme}%"])
        
#         where_query = " AND ".join([f"({part}" for part in where_parts])
        
#         # Requête SQL complète avec jointures
#         query = f"""
#             SELECT 
#                 d.*,
#                 f.source,
#                 e.vol, e.tom, e.num, e.date_edition, e.pages, e.ville_edition, e.editeur,
#                 GROUP_CONCAT(a.auteur SEPARATOR ' & ') as auteurs
#             FROM 
#                 doc d
#                 INNER JOIN fournit f ON d.n_enregistrement = f.n_enregistrement
#                 INNER JOIN edition e ON d.n_enregistrement = e.n_enregistrement
#                 INNER JOIN ecriture a ON d.n_enregistrement = a.n_enregistrement
#             WHERE 
#                 {where_query}
#             GROUP BY 
#                 d.n_enregistrement
#             ORDER BY
#                 d.titre
#         """
        
#         # Exécution de la requête
#         with connection.cursor() as cursor:
#             cursor.execute(query, params)
#             columns = [col[0] for col in cursor.description]
#             documents = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
#         # Préparation des résultats pour le template
#         for doc in documents:
#             doc['est_periodique'] = doc['periodicite'] == 'p'
        
#         return render(request, 'search.html', {
#             'documents': documents,
#             'terme_recherche': terme_recherche
#         })
    
#     return render(request, 'search.html')

from django.shortcuts import render
from django.db import connection

# def resultatSearch(request):
#     documents = []
#     terme_recherche = ''

#     if request.method == 'GET' and 'q' in request.GET:
#         terme_recherche = request.GET['q'].strip()
#         termes = terme_recherche.lower().split()

#         where_parts = []
#         params = []
#         for terme in termes:
#             where_parts.append("((LOWER(d.titre) LIKE %s) OR (LOWER(d.titre_article) LIKE %s))")
#             params.extend([f"%{terme}%", f"%{terme}%"])

#         where_query = " AND ".join([f"({part}" for part in where_parts])

#         query = f"""
#             SELECT 
#                 d.*,
#                 f.source,
#                 e.vol, e.tom, e.num, e.date_edition, e.pages, e.ville_edition, e.editeur,
#                 GROUP_CONCAT(a.auteur SEPARATOR ' & ') as auteurs
#             FROM 
#                 doc d
#                 INNER JOIN fournit f ON d.n_enregistrement = f.n_enregistrement
#                 INNER JOIN edition e ON d.n_enregistrement = e.n_enregistrement
#                 INNER JOIN ecriture a ON d.n_enregistrement = a.n_enregistrement
#             WHERE 
#                 {where_query}
#             GROUP BY 
#                 d.n_enregistrement
#             ORDER BY
#                 d.titre
#         """

#         with connection.cursor() as cursor:
#             cursor.execute(query, params)
#             columns = [col[0] for col in cursor.description]
#             documents = [dict(zip(columns, row)) for row in cursor.fetchall()]

#         for doc in documents:
#             doc['est_periodique'] = doc.get('periodicite') == 'p'

#     return render(request, 'search.html', {
#         'documents': documents,
#         'terme_recherche': terme_recherche,
#     })

# def resultatSearch(request):
#     documents = []
#     terme_recherche = ''

#     if request.method == 'GET' and 'q' in request.GET:
#         terme_recherche = request.GET['q'].strip()
#         termes = terme_recherche.lower().split()

#         where_parts = []
#         params = []
#         for terme in termes:
#             where_parts.append("((LOWER(d.titre) LIKE %s) OR (LOWER(d.titre_article) LIKE %s))")
#             params.extend([f"%{terme}%", f"%{terme}%"])

#         # Fermeture correcte des parenthèses
#         where_query = " AND ".join([f"({part})" for part in where_parts])

#         query = f"""
#             SELECT 
#                 d.*,
#                 f.source,
#                 d.vol, d.tom, d.num, e.date_edition, d.pages, e.ville_edition, e.editeur,
#                 GROUP_CONCAT(a.auteur SEPARATOR ' & ') as auteurs
#             FROM 
#                 doc d
#                 INNER JOIN fournit f ON d.n_enregistrement = f.n_enregistrement
#                 INNER JOIN edition e ON d.n_enregistrement = e.n_enregistrement
#                 INNER JOIN ecriture a ON d.n_enregistrement = a.n_enregistrement
#             WHERE 
#                 {where_query}
#             GROUP BY 
#                 d.n_enregistrement
#             ORDER BY
#                 d.titre
#         """

#         with connection.cursor() as cursor:
#             cursor.execute(query, params)
#             columns = [col[0] for col in cursor.description]
#             documents = [dict(zip(columns, row)) for row in cursor.fetchall()]

#         for doc in documents:
#             doc['est_periodique'] = doc.get('periodicite') == 'p'

#     return render(request, 'search.html', {
#         'documents': documents,
#         'terme_recherche': terme_recherche,
#     })

def resultatSearch(request):
    documents = []
    terme_recherche = ''
    formSearch = SearchForm(request.GET or None)
    if request.method == 'GET' and 'q' in request.GET:
        terme_recherche = request.GET['q'].strip()
        termes = terme_recherche.lower().split()

        where_parts = []
        params = []
        for terme in termes:
            where_parts.append("((LOWER(d.titre) LIKE %s) OR (LOWER(d.titre_article) LIKE %s))")
            params.extend([f"%{terme}%", f"%{terme}%"])

        # Ici on utilise OR entre chaque condition (au moins un mot doit être présent)
        where_query = " OR ".join([f"({part})" for part in where_parts]) if where_parts else "1=1"

        query = f"""
            SELECT 
                d.*,
                f.source,
                d.vol, d.tom, d.num, e.date_edition, d.pages, e.ville_edition, e.editeur,
                GROUP_CONCAT(a.auteur SEPARATOR ' & ') as auteurs
            FROM 
                doc d
                INNER JOIN fournit f ON d.n_enregistrement = f.n_enregistrement
                INNER JOIN edition e ON d.n_enregistrement = e.n_enregistrement
                INNER JOIN ecriture a ON d.n_enregistrement = a.n_enregistrement
            WHERE 
                {where_query}
            GROUP BY 
                d.n_enregistrement
            ORDER BY
                d.titre
        """

        with connection.cursor() as cursor:
            cursor.execute(query, params)
            columns = [col[0] for col in cursor.description]
            documents = [dict(zip(columns, row)) for row in cursor.fetchall()]

        for doc in documents:
            doc['est_periodique'] = doc.get('periodicite') == 'p'

    return render(request, 'search.html', {
        'documents': documents,
        'terme_recherche': terme_recherche,
        'formSearch': formSearch,
    })


