from django.shortcuts import render
from datetime import datetime
# Create your views here.
def collecte(request):
    return render(request, 'collecte.html')
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection
from django.views import View
from .forms import PeriodiqueForm

from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection
from django.views import View
from .forms import PeriodiqueForm, MonographieForm,  SearchForm, CollectDocForm, CollectLoginForm

# class PeriodiqueAuthView(View):
#     template_name = 'logins/periodique.html'
#     form_class = PeriodiqueForm

#     def get(self, request):
#         form_periodique = self.form_class()
#         return render(request, self.template_name, {'form_periodique': form_periodique})

#     def post(self, request):
#         form_periodique = self.form_class(request.POST)
        
#         if form_periodique.is_valid():
#             username = form_periodique.cleaned_data['username']
#             password = form_periodique.cleaned_data['password']
            
#             with connection.cursor() as cursor:
#                 cursor.execute(
#                     "SELECT 1 FROM admin WHERE login = %s AND pass = %s AND destination = 'collecte'",
#                     [username, password]
#                 )
#                 if cursor.fetchone():
#                     # Créer un token unique à chaque connexion
#                     request.session['periodique_auth_token'] = f"token_{username}_{request.session.session_key}"
#                     return redirect('periodique_protected')
#                 else:
#                     messages.error(request, "Saisie incorrecte ou module non autorisé.")
        
#         return render(request, self.template_name, {'form_periodique': form_periodique})
class PeriodiqueAuthView(View):
    template_name = 'logins/periodique.html'
    form_class = PeriodiqueForm

    # def get(self, request):
    #     form_periodique = self.form_class()
    #     return render(request, self.template_name, {'form_periodique': form_periodique})
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
from .forms import ArticlePeriodiqueForm, SearchForm, NonPeriodiqueForm
from django.contrib import messages
from Main.models import Doc, Ecriture, Edition, Fournit, Collecte, Suivi, Indexation
from django.urls import reverse
class PeriodiqueProtectedView(View):
    template_name = 'periodique.html'

    # def dispatch(self, request, *args, **kwargs):
    #     # Vérification stricte + suppression immédiate de l'authentification
    #     if not request.session.get('periodique_auth_token'):
    #         return redirect('periodique_login ')
    #     # Supprimer le token immédiatement après vérification
    #     token = request.session.pop('periodique_auth_token', None)
    #     if not token:
    #         return redirect('periodique_login')
            
    #     return super().dispatch(request, *args, **kwargs)
    def get(self, request):
        # Initialisation des formulaires
        formSearch = SearchForm(request.GET or None)
        article_form = ArticlePeriodiqueForm(initial={
            'titre': request.session.get('titre_document', ''),
            'source_expeditrice': request.session.get('source', ''),
        })
        context = {
            'formSearch': formSearch,
            'article_form': article_form,
            'source_expeditrice' : request.session.get('source', '')
        }
        return render(request, self.template_name, context)
    def post(self, request):
        article_form = ArticlePeriodiqueForm(request.POST)
        formSearch = SearchForm(request.GET or None)
        
        if article_form.is_valid():
            try:
                cursor = connection.cursor()
                # Récupérer les infos du document collecté
                cursor.execute(
                    """
                    SELECT titre_document, source_document, support_document 
                    FROM doc_collecte 
                    WHERE n_enregistrement = %s
                    """,
                    [article_form.cleaned_data['n_enregistrement']]
                )
                row = cursor.fetchone()
                titre_document, source_document, support_document = row if row else (None, None, None)

                # Mettre à jour le statut
                cursor.execute(
                    """
                    UPDATE doc_collecte SET statut = 'Enregistré' WHERE n_enregistrement = %s
                    """,
                    [article_form.cleaned_data['n_enregistrement']]
                )
                cursor.execute(
                    """
                    INSERT INTO doc_article (
                        n_enregistrement, titre, titre_article, pages, domaine, vol, tom, num,statut, n_periodique, lang, type_support, acces, id_acces_arabe, id_acces_etranger
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    [
                        article_form.cleaned_data['n_enregistrement'],
                        article_form.cleaned_data['titre'],
                        titre_document,
                        article_form.cleaned_data['pages'],
                        article_form.cleaned_data['domaine'],
                        article_form.cleaned_data['vol'],
                        article_form.cleaned_data['tom'],
                        article_form.cleaned_data['num'],
                        'Enregistré',
                        article_form.cleaned_data['n_periodicite'],
                        article_form.cleaned_data['langue'],
                        support_document,
                        article_form.cleaned_data['acces'],
                        article_form.cleaned_data['id_acces_arabe'],
                        article_form.cleaned_data['id_acces_etranger'],
                    ]
                )
                n_enregistrement = article_form.cleaned_data['n_enregistrement']
                auteurs = article_form.cleaned_data['auteurs'].split('/')
                for auteur in auteurs:
                    auteur = auteur.strip()
                    if auteur:
                        cursor.execute(
                            """
                            INSERT INTO auteur (auteur, n_enregistrement) VALUES (%s, %s)
                            """,
                            [auteur, n_enregistrement]
                        )
                cursor.execute(
                    """
                    INSERT INTO fournit(source, n_enregistrement, date_reception, obligation)
                    VALUES (%s, %s, %s, %s)
                    """,
                    [
                        source_document,
                        article_form.cleaned_data['n_enregistrement'],
                        article_form.cleaned_data['date_reception'],
                        article_form.cleaned_data['type_acquisition']
                    ]
                )
                cursor.execute(
                    """
                    INSERT INTO collecte(nomrc, n_enregistrement, datsaisi_c)
                    VALUES (%s, %s, %s)
                    """,
                    [
                        article_form.cleaned_data['responsable_saisie'],
                        article_form.cleaned_data['n_enregistrement'],
                        date.today()
                    ]
                )

                # Insérer dans doc_enregistre
                cursor.execute(
                    """
                    INSERT INTO doc_enregistre(responsable_saisie, statut, n_enregistrement, date_saisie)
                    VALUES (%s, %s, %s, %s)
                    """,
                    [
                        article_form.cleaned_data['responsable_saisie'],
                        'Enregistré',
                        article_form.cleaned_data['n_enregistrement'],
                        date.today()
                    ]
                )
                # Sauvegarde dans la table Doc
                # doc = Doc.objects.create(
                #     n_enregistrement=article_form.cleaned_data['n_enregistrement'],
                #     titre=article_form.cleaned_data['titre'],
                #     titre_article=article_form.cleaned_data['titre_article'],
                #     periodicite='p',  # Périodique
                #     vol=article_form.cleaned_data['vol'],
                #     tom=article_form.cleaned_data['tom'],
                #     num=article_form.cleaned_data['num'],
                #     pages=article_form.cleaned_data['pages'],
                #     domaine=article_form.cleaned_data['domaine'].domaine,
                #     statut='collecte',
                #     lang=article_form.cleaned_data['langue'],
                # )
                
                # # Gestion des auteurs (séparés par /)
                # auteurs = article_form.cleaned_data['auteurs'].split('/')
                # for auteur in auteurs:
                #     if auteur.strip():  # Ignore les chaînes vides
                #         Ecriture.objects.create(
                #             auteur=auteur.strip(),
                #             n_enregistrement=doc.n_enregistrement
                #         )
                
                # # Sauvegarde dans Edition
                # if article_form.cleaned_data['editeur']:
                #     Edition.objects.create(
                #         editeur=article_form.cleaned_data['editeur'].editeur,
                #         n_enregistrement=doc.n_enregistrement,
                #     )
                
                # # Sauvegarde dans Fournit
                # Fournit.objects.create(
                #     source=article_form.cleaned_data['source_expeditrice'].source,
                #     n_enregistrement=doc.n_enregistrement,
                #     date_reception=article_form.cleaned_data['date_reception'],
                #     obligation=article_form.cleaned_data['type_acquisition']
                # )
                
                # # Sauvegarde dans Collecte
                # Collecte.objects.create(
                #     nomrc=article_form.cleaned_data['responsable_saisie'],
                #     n_enregistrement=doc.n_enregistrement,
                #     datsaisi_c=article_form.cleaned_data['date_saisie']
                # )
                
                # # Sauvegarde dans Suivi
                # Suivi.objects.create(
                #     noms=article_form.cleaned_data['responsable_saisie'],
                #     n_enregistrement=doc.n_enregistrement,
                #     datenvoi_t=article_form.cleaned_data['date_envoi']
                # )
                
                messages.success(request, "L'article périodique a été enregistré avec succès!")
                article_form = ArticlePeriodiqueForm()  # 
            
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

from datetime import date
class MonographieProtectedView(View):
    template_name = 'monographie.html'

    # def dispatch(self, request, *args, **kwargs):
    #     if not request.session.get('monographie_auth_token'):
    #         return redirect('monographie_login')
    #     token = request.session.pop('monographie_auth_token', None)
    #     if not token:
    #         return redirect('monographie_login')
    #     return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        formSearch = SearchForm(request.GET or None)
        monographie_form = NonPeriodiqueForm(initial={
            'titre_article': request.session.get('titre_document', ''),
            'source_expeditrice': request.session.get('source', ''),
        })

        context = {
            'formSearch': formSearch,
            'monographie_form': monographie_form,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        monographie_form = NonPeriodiqueForm(request.POST)
        formSearch = SearchForm(request.GET or None)

        if monographie_form.is_valid():
            try:
                cursor = connection.cursor()
                # Récupérer les infos du document collecté
                cursor.execute(
                    """
                    SELECT titre_document, source_document, support_document 
                    FROM doc_collecte 
                    WHERE n_enregistrement = %s
                    """,
                    [monographie_form.cleaned_data['n_enregistrement']]
                )
                row = cursor.fetchone()
                titre_document, source_document, support_document = row if row else (None, None, None)

                # Mettre à jour le statut
                cursor.execute(
                    """
                    UPDATE doc_collecte SET statut = 'Enregistré' WHERE n_enregistrement = %s
                    """,
                    [monographie_form.cleaned_data['n_enregistrement']]
                )

                # Insérer dans doc_monographie
                cursor.execute(
                    """
                    INSERT INTO doc_monographie (
                        n_enregistrement, titre, pages, domaine, type, statut, n_periodique, lang, type_support, acces, id_acces_arabe, id_acces_etranger, source
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    [
                        monographie_form.cleaned_data['n_enregistrement'],
                        titre_document,
                        monographie_form.cleaned_data['pages'],
                        monographie_form.cleaned_data['domaine'],
                        monographie_form.cleaned_data['type'],
                        'Enregistré',
                        monographie_form.cleaned_data['n_periodicite'],
                        monographie_form.cleaned_data['langue'],
                        support_document,
                        monographie_form.cleaned_data['acces'],
                        monographie_form.cleaned_data['id_acces_arabe'],
                        monographie_form.cleaned_data['id_acces_etranger'],
                        monographie_form.cleaned_data['source_expeditrice'],
                    ]
                )

                # Insérer les auteurs
                n_enregistrement = monographie_form.cleaned_data['n_enregistrement']
                auteurs = monographie_form.cleaned_data['auteurs'].split('/')
                for auteur in auteurs:
                    auteur = auteur.strip()
                    if auteur:
                        cursor.execute(
                            """
                            INSERT INTO auteur (auteur, n_enregistrement) VALUES (%s, %s)
                            """,
                            [auteur, n_enregistrement]
                        )

                # Insérer dans editeur
                cursor.execute(
                    """
                    INSERT INTO editeur(editeur, ville_edition, n_enregistrement, date_edition)
                    VALUES (%s, %s, %s, %s)
                    """,
                    [
                        monographie_form.cleaned_data['editeur'],
                        monographie_form.cleaned_data['ville_edition'],
                        monographie_form.cleaned_data['n_enregistrement'],
                        monographie_form.cleaned_data['date_edition'],
                    ]
                )

                # Insérer dans fournit
                # cursor.execute(
                #     """
                #     INSERT INTO fournit(source, n_enregistrement, date_reception, obligation)
                #     VALUES (%s, %s, %s, %s)
                #     """,
                #     [
                #         source_document,
                #         monographie_form.cleaned_data['n_enregistrement'],
                #         monographie_form.cleaned_data['date_reception'],
                #         monographie_form.cleaned_data['type_acquisition']
                #     ]
                # )

                # Insérer dans collecte
                # cursor.execute(
                #     """
                #     INSERT INTO collecte(nomrc, n_enregistrement, datsaisi_c)
                #     VALUES (%s, %s, %s)
                #     """,
                #     [
                #         monographie_form.cleaned_data['responsable_saisie'],
                #         monographie_form.cleaned_data['n_enregistrement'],
                #         date.today()
                #     ]
                # )

                # Insérer dans doc_enregistre
                cursor.execute(
                    """
                    INSERT INTO doc_enregistre(responsable_saisie, statut, n_enregistrement, date_saisie)
                    VALUES (%s, %s, %s, %s)
                    """,
                    [
                        monographie_form.cleaned_data['responsable_saisie'],
                        'Enregistré',
                        monographie_form.cleaned_data['n_enregistrement'],
                        date.today()
                    ]
                )

                messages.success(request, "La monographie a été enregistrée avec succès!")
                monographie_form = NonPeriodiqueForm()

            except Exception as e:
                messages.error(request, f"Une erreur est survenue: {str(e)}")

        context = {
            'formSearch': formSearch,
            'monographie_form': monographie_form,
        }
        return render(request, self.template_name, context)


def monographie_logout(request):
    request.session.flush()
    return redirect('monographie_login')

from django.db.models import Count

# Partie Indexeur
# class IndexeurAuthView(View):
#     template_name = 'logins/indexeur.html'
#     form_class = IndexeurForm

#     def get(self, request):
#         form_indexeur = self.form_class()
#         return render(request, self.template_name, {'form_indexeur': form_indexeur})

#     def post(self, request):
#         form_indexeur = self.form_class(request.POST)
        
#         if form_indexeur.is_valid():
#             username = form_indexeur.cleaned_data['username']
#             password = form_indexeur.cleaned_data['password']
            
#             with connection.cursor() as cursor:
#                 cursor.execute(
#                     "SELECT 1 FROM admin WHERE login = %s AND pass = %s AND destination = 'suivi'",
#                     [username, password]
#                 )
#                 if cursor.fetchone():
#                     # Créer un token unique à chaque connexion
#                     request.session['indexeur_auth_token'] = f"token_{username}_{request.session.session_key}"
#                     return redirect('indexeur_protected')
#                 else:
#                     messages.error(request, "Saisie incorrecte ou module non autorisé.")
        
#         return render(request, self.template_name, {'form_indexeur': form_indexeur})

###################################################################################################""""
# class IndexeurProtectedView(View):
#     template_name = 'indexeur.html'
    
#     def dispatch(self, request, *args, **kwargs):
#         # Vérification stricte + suppression immédiate de l'authentification
#         if not request.session.get('indexeur_auth_token'):
#             return redirect('indexeur_login')
        
#         # Supprimer le token immédiatement après vérification
#         token = request.session.pop('indexeur_auth_token', None)
#         if not token:
#             return redirect('indexeur_login')
            
#         return super().dispatch(request, *args, **kwargs)
#     def post(self, request):
#         formIndexeur = IndexeurContentForm(request.POST)
#         if formIndexeur.is_valid():
#             try:
#                 with connection.cursor() as cursor:
#                     cursor.execute(
#                         "INSERT INTO indexeur (n_enregistrement, nomi) VALUES (%s, %s)",[formIndexeur.cleaned_data['n_enregistrement'], formIndexeur.cleaned_data['nomi']]
#                     )
#                     cursor.execute(
#                         "UPDATE doc SET statut = 'suivi1' WHERE n_enregistrement = %s", [formIndexeur.cleaned_data['n_enregistrement']]
#                     )
#                 messages.success(request, "Document affecté avec succès!")
#                 return redirect('indexeur_protected')
#             except Exception as e:
#                 messages.error(request, f"Erreur lors de l'affectation du document: {str(e)}")

#         return render(request, self.template_name, {'formIndexeur': formIndexeur})
    
#     def get(self, request):
#         with connection.cursor() as cursor:
#             cursor.execute("""
#                 SELECT i.nomi, COUNT(i.n_enregistrement) AS nombre
#                 FROM indexation i
#                 INNER JOIN doc d ON i.n_enregistrement = d.n_enregistrement
#                 WHERE d.statut = %s
#                 GROUP BY i.nomi
#                 ORDER BY i.nomi
#             """, ['suivi1'])
#             rows = cursor.fetchall()
#             indexeurs = [
#                 {'nomi': row[0], 'nombre': row[1]}
#                 for row in rows
#             ] if rows else []
#         context = {
#             'formIndexeur': IndexeurContentForm(),
#             'formSearch': SearchForm(request.GET or None),
#             'indexeurs': indexeurs,  # Toujours une liste
#         }
#         return render(request, self.template_name, context)


# def indexeur_logout(request):
#     request.session.flush()
#     return redirect('indexeur_login')


# # Partie Indexation et Controle
# class IndexationControlAuthView(View):
#     template_name = 'logins/indexationControl.html'
#     form_class = IndexationControlForm

#     def get(self, request):
#         form_indexationControl = self.form_class()
#         return render(request, self.template_name, {'form_indexationControl': form_indexationControl})

#     def post(self, request):
#         form_indexationControl = self.form_class(request.POST)
        
#         if form_indexationControl.is_valid():
#             username = form_indexationControl.cleaned_data['username']
#             password = form_indexationControl.cleaned_data['password']
            
#             with connection.cursor() as cursor:
#                 cursor.execute(
#                     "SELECT 1 FROM admin WHERE login = %s AND pass = %s AND destination = 'indexation'",
#                     [username, password]
#                 )
#                 if cursor.fetchone():
#                     # Créer un token unique à chaque connexion
#                     request.session['indexationControl_auth_token'] = f"token_{username}_{request.session.session_key}"
#                     return redirect('indexationControl_protected')
#                 else:
#                     messages.error(request, "Saisie incorrecte ou module non autorisé.")
        
#         return render(request, self.template_name, {'form_indexationControl': form_indexationControl})


# class IndexationControlProtectedView(View):
#     template_name = 'indexationControl.html'
    
#     def dispatch(self, request, *args, **kwargs):
#         # Vérification stricte + suppression immédiate de l'authentification
#         if not request.session.get('indexationControl_auth_token'):
#             return redirect('indexationControl_login')
        
#         # Supprimer le token immédiatement après vérification
#         token = request.session.pop('indexationControl_auth_token', None)
#         if not token:
#             return redirect('indexationControl_login')
            
#         return super().dispatch(request, *args, **kwargs)
    
#     def get(self, request):
#         # Initialisation des formulaires
#         formSearch = SearchForm(request.GET or None)
#         formIndexationControlContent = IndexationControlContentForm()
        
#         context = {
#             'formSearch': formSearch,
#             'formIndexationControlContent': formIndexationControlContent,
#         }
#         return render(request, self.template_name, context)
    
#     def post(self, request):
#         formIndexationControlContent = IndexationControlContentForm(request.POST)
#         if formIndexationControlContent.is_valid():
#                 try:
#                     n_enregistrement = formIndexationControlContent.cleaned_data['n_enregistrement']
#                     # Récupérer nomi depuis la table indexeur
#                     with connection.cursor() as cursor:
#                         cursor.execute(
#                             "SELECT nomi FROM indexeur WHERE n_enregistrement = %s", [n_enregistrement]
#                         )
#                         result = cursor.fetchone()
#                         if not result:
#                             messages.error(request, "Aucun indexeur trouvé pour ce document.")
#                             return render(request, self.template_name, {'formIndexationControlContent': formIndexationControlContent})
#                         nomi = result[0]
#                         # Insérer dans indexation
#                         cursor.execute(
#                             "INSERT INTO indexation (n_enregistrement, nomi, dat_reception, dat_indexation, dat_saisi, dat_envoi) VALUES (%s, %s, %s, %s, %s, %s)",
#                             [
#                                 n_enregistrement,
#                                 nomi,
#                                 formIndexationControlContent.cleaned_data['dat_recep_pour_indexation'],
#                                 datetime.today().strftime('%Y-%m-%d'),
#                                 datetime.today().strftime('%Y-%m-%d'),
#                                 formIndexationControlContent.cleaned_data['dat_envoi_control']
#                             ]
#                         )
#                         cursor.execute(
#                             """INSERT INTO control (
#                                 n_enregistrement, 
#                                 nomc, 
#                                 dat_ctrl, 
#                                 observation, 
#                                 retourne, 
#                                 dat_valid, 
#                                 dat_recepc) VALUES (%s, %s, %s, %s, %s, %s, %s)""",
#                             [
#                                 n_enregistrement,
#                                 formIndexationControlContent.cleaned_data['nomc'],
#                                 datetime.today().strftime('%Y-%m-%d'),
#                                 formIndexationControlContent.cleaned_data['observation'],
#                                 'Non',
#                                  # Partie enlever du formulaire
#                                 # formIndexationControl.cleaned_data['dat_retour_correc'],
#                                 datetime.today().strftime('%Y-%m-%d'),
#                                 formIndexationControlContent.cleaned_data['dat_recep_pour_controle'],
#                             ]
#                         )
#                         cursor.execute(
#                                  "SELECT dat_rsuivi FROM controle WHERE n_enregistrement = %s",
#                                  [n_enregistrement]
#                              )
#                         result = cursor.fetchone()
#                         dat_rsuivi = result[0] if result else None
#                         cursor.execute(
#                             "UPDATE suivi SET noms = %s, datsaisi_ic = %s, dat_rsuivi = %s WHERE n_enregistrement = %s",
#                             [
#                                 formIndexationControlContent.cleaned_data['noms'],
#                                 formIndexationControlContent.cleaned_data['dat_envoi_suivi'],
#                                 n_enregistrement
#                             ]
#                         )
#                         cursor.execute(
#                             """
#                             UPDATE doc SET statut = %s WHERE n_enregistrement
#                             """,
#                             [
#                                 "suivi2"
#                             ]
#                         )
                 
#                     messages.success(request, "Document affecté avec succès!")
#                     return redirect('indexationControl_protected')
#                 except Exception as e:
#                     messages.error(request, f"Erreur lors de l'affectation du document: {str(e)}")
#         return render(request, self.template_name, {'formIndexationControlContent': formIndexationControlContent})
##########################################################################################################################""""""
    # def post(self, request):
    #     formIndexationControl1 = IndexationControlContentForm1(request.POST)
    #     formIndexationControl2 = IndexationControlContentForm2(request.POST)
    #     formIndexationControl3 = IndexationControlContentForm3(request.POST)
    #     if formIndexationControl1.is_valid():
    #         try:
    #             n_enregistrement = formIndexationControl1.cleaned_data['n_enregistrement']
    #             # Récupérer nomi depuis la table indexeur
    #             with connection.cursor() as cursor:
    #                 cursor.execute(
    #                     "SELECT nomi FROM indexeur WHERE n_enregistrement = %s", [n_enregistrement]
    #                 )
    #                 result = cursor.fetchone()
    #                 if not result:
    #                     messages.error(request, "Aucun indexeur trouvé pour ce document.")
    #                     return render(request, self.template_name, {'formIndexationControl': formIndexationControl1})
    #                 nomi = result[0]
    #                 # Insérer dans indexation
    #                 cursor.execute(
    #                     "INSERT INTO indexation (n_enregistrement, nomi, dat_reception, dat_indexation, dat_saisi, dat_envoi) VALUES (%s, %s, %s, %s, %s, %s)",
    #                     [
    #                         n_enregistrement,
    #                         nomi,
    #                         formIndexationControl1.cleaned_data['dat_recep'],
    #                         formIndexationControl1.cleaned_data['dat_index'],
    #                         formIndexationControl1.cleaned_data['dat_saisi'],
    #                         formIndexationControl1.cleaned_data['dat_envoi']
    #                     ]
    #                 )
    #             messages.success(request, "Document affecté avec succès!")
    #             return redirect('indexationControl_protected')
    #         except Exception as e:
    #             messages.error(request, f"Erreur lors de l'affectation du document: {str(e)}")

    #     if formIndexationControl2.is_valid():
    #         try:
    #             n_enregistrement = formIndexationControl2.cleaned_data['n_enregistrement']
    #             # Récupérer nomi depuis la table indexeur
    #             with connection.cursor() as cursor:
    #                 cursor.execute(
    #                     "INSERT INTO control (n_enregistrement, nomc, dat_ctrl, observation, retourne, dat_retour, dat_valid, visa, dat_recep_control) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
    #                     [
    #                         n_enregistrement,
    #                         formIndexationControl2.cleaned_data['nomc'],
    #                         formIndexationControl2.cleaned_data['dat_control'],
    #                         formIndexationControl2.cleaned_data['observation'],
    #                         formIndexationControl2.cleaned_data['retour_correc'],
    #                         formIndexationControl2.cleaned_data['dat_retour_correc'],
    #                         formIndexationControl2.cleaned_data['dat_validation'],
    #                         formIndexationControl2.cleaned_data['visa'],
    #                         formIndexationControl2.cleaned_data['date_recep_control'],
    #                     ]
    #                 )
    #             messages.success(request, "Document affecté avec succès!")
    #             return redirect('indexationControl_protected')
    #         except Exception as e:
    #             messages.error(request, f"Erreur lors de l'affectation du document: {str(e)}")
        
    #     if formIndexationControl3.is_valid():
    #         try:
    #             n_enregistrement = formIndexationControl3.cleaned_data['n_enregistrement']
    #             # Récupérer nomi depuis la table indexeur
    #             with connection.cursor() as cursor:
    #                 cursor.execute(
    #                             "SELECT dat_rsuivi FROM controle WHERE n_enregistrement = %s",
    #                             [n_enregistrement]
    #                         )
    #                 result = cursor.fetchone()
    #                 dat_rsuivi = result[0] if result else None

    #                 cursor.execute(
    #                     "UPDATE suivi SET noms = %s, datsaisi_c = %s, datenvoi_sir = %s, dat_rsuivi = %s WHERE n_enregistrement = %s",
    #                     [
    #                         formIndexationControl3.cleaned_data['noms'],
    #                         formIndexationControl3.cleaned_data['dat_suivi'],
    #                         formIndexationControl3.cleaned_data['dat_envoi_SIR'],
    #                         dat_rsuivi,
    #                         n_enregistrement
    #                     ]
    #                 )
    #             messages.success(request, "Document affecté avec succès!")
    #             return redirect('indexationControl_protected')
    #         except Exception as e:
    #             messages.error(request, f"Erreur lors de l'affectation du document: {str(e)}")


    #     return render(request, self.template_name, {'formIndexationControl': formIndexationControl1})

# def indexationControl_logout(request):
#     request.session.flush()
#     return redirect('indexationControl_login')


# # Partie Prise de Vue
# class PriseVueAuthView(View):
#     template_name = 'logins/priseVue.html'
#     form_class = PriseVueForm

#     def get(self, request):
#         form_priseVue = self.form_class()
#         return render(request, self.template_name, {'form_priseVue': form_priseVue})

#     def post(self, request):
#         form_priseVue = self.form_class(request.POST)
        
#         if form_priseVue.is_valid():
#             username = form_priseVue.cleaned_data['username']
#             password = form_priseVue.cleaned_data['password']
            
#             with connection.cursor() as cursor:
#                 cursor.execute(
#                     "SELECT 1 FROM admin WHERE login = %s AND pass = %s AND destination = 'vue'",
#                     [username, password]
#                 )
                
#                 if cursor.fetchone():
#                     # Créer un token unique à chaque connexion
#                     request.session['priseVue_auth_token'] = f"token_{username}_{request.session.session_key}"
#                     return redirect('priseVue_protected')
#                 else:
#                     messages.error(request, "Saisie incorrecte ou module non autorisé.")
        
#         return render(request, self.template_name, {'form_priseVue': form_priseVue})


# class PriseVueProtectedView(View):
#     template_name = 'priseVue.html'
    
#     def dispatch(self, request, *args, **kwargs):
#         # Vérification stricte + suppression immédiate de l'authentification
#         if not request.session.get('priseVue_auth_token'):
#             return redirect('priseVue_login')
        
#         # Supprimer le token immédiatement après vérification
#         token = request.session.pop('priseVue_auth_token', None)
#         if not token:
#             return redirect('priseVue_login')
            
#         return super().dispatch(request, *args, **kwargs)
#     def post(self, request):
#         formPriseDeVueContentForm = PriseDeVueContentForm(request.POST)
#         if formPriseDeVueContentForm.is_valid():
#                 try:
#                     n_enregistrement = formPriseDeVueContentForm.cleaned_data['n_enregistrement']
#                     # Récupérer nomi depuis la table indexeur
#                     with connection.cursor() as cursor:
#                         cursor.execute(
#                             "UPDATE suivi SET dat_pv = %s, dat_rrsuivi = %s, dat_mont = %s, datsaisi_pv = %s WHERE n_enregistrement = %s",
#                             [
#                                 datetime.today().strftime('%Y-%m-%d'),
#                                 formPriseDeVueContentForm.cleaned_data['dat_envoi_bibliotheque'],
#                                 datetime.today().strftime('%Y-%m-%d'),
#                                 datetime.today().strftime('%Y-%m-%d'),
#                                 n_enregistrement
#                             ]
#                         )
#                         cursor.execute(
#                             """SELECT nomc, dat_ctrl, visa FROM control WHERE n_enregistrement = %s,
#                             """,
#                             [
#                                 n_enregistrement 
#                             ]
#                         )
#                         result = cursor.fetchone()
#                         dat_ctrl = result[1] if result else None
#                         nomc = result[0] if result else None
#                         visa = result[2] if result else None
#                         cursor.execute(
#                                  """
#                                  INSERT INTO vue (
#                                      n_enregistrement, 
#                                      dat_ctrl, 
#                                      visa, 
#                                      controleur,
#                                      dat_recepv
#                                      ) VALUES (%s, %s, %s, %s, %s)
#                                  """, [
#                                      n_enregistrement,
#                                      dat_ctrl,
#                                      visa,
#                                      nomc,
#                                      formPriseDeVueContentForm.cleaned_data['dat_recep_vue'],
#                                  ]
#                              )
                    
#                         cursor.execute(
#                             """
#                             UPDATE doc SET statut = %s WHERE n_enregistrement
#                             """,
#                             [
#                                 "fini"
#                             ]
#                         )
                 
#                     messages.success(request, "Document affecté avec succès!")
#                     return redirect('priseVue_protected')
#                 except Exception as e:
#                     messages.error(request, f"Erreur lors de l'affectation du document: {str(e)}")
#         return render(request, self.template_name, {'formPriseDeVueContent': formPriseDeVueContentForm})
#     def get(self, request):
#         formSearch = SearchForm(request.GET or None)
#         formPriseDeVueContentForm = PriseDeVueContentForm()
        
#         context = {
#             'formSearch': formSearch,
#             'formPriseDeVueContent': formPriseDeVueContentForm,
#         }
#         return render(request, self.template_name, context)


# def priseVue_logout(request):
#     request.session.flush()
#     return redirect('priseVue_login')




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

#         where_query = " AND ".join([f"({part})" for part in where_parts])

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


class CollectAuthView(View):
    template_name = 'logins/collection.html'
    form_class = CollectLoginForm

    def get(self, request):
        form_collect = self.form_class()
        return render(request, self.template_name, {'form_collect': form_collect})

    def post(self, request):
        form_collect = self.form_class(request.POST)
        
        if form_collect.is_valid():
            username = form_collect.cleaned_data['username']
            password = form_collect.cleaned_data['password']
            
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT 1 FROM admin WHERE login = %s AND pass = %s AND destination = 'collecte'",
                    [username, password]
                )
                if cursor.fetchone():
                    # Créer un token unique à chaque connexion
                    request.session['collect_auth_token'] = f"token_{username}_{request.session.session_key}"
                    return redirect('collect_protected')
                else:
                    messages.error(request, "Saisie incorrecte ou module non autorisé.")
        
        return render(request, self.template_name, {'form_collect': form_collect})
    

class CollectDocView(View):
    template_name = 'collection.html'

    def get(self, request):
        formSearch = SearchForm(request.GET or None)
        form_collection_doc = CollectDocForm()
        context = {
            'formSearch': formSearch,
            'form_collection_doc': form_collection_doc,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form_collection_doc = CollectDocForm(request.POST)
        formSearch = SearchForm(request.GET or None)

        if form_collection_doc.is_valid():
            request.session['titre_document'] = form_collection_doc.cleaned_data['titre_document']
            request.session['source'] = form_collection_doc.cleaned_data['source']
            try:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO doc_collecte(
                            titre_document,
                            source_document,
                            support_document,
                            date_collecte,
                            statut
                        )
                        VALUES (%s, %s, %s, %s, %s)
                        """,
                        [
                            form_collection_doc.cleaned_data['titre_document'],
                            form_collection_doc.cleaned_data['source'],
                            form_collection_doc.cleaned_data['support'],
                            form_collection_doc.cleaned_data['date_collect'],
                            'Collecté'
                        ]
                    )
                    connection.commit()
                messages.success(request, "Document collecté avec succès!")

                # Réinitialiser le formulaire après succès
                form_collection_doc = CollectDocForm()

            except Exception as e:
                connection.rollback()
                messages.error(request, f"Une erreur est survenue: {str(e)}")

        context = {
            'formSearch': formSearch,
            'form_collection_doc': form_collection_doc,
        }
        return render(request, self.template_name, context)
