from django.shortcuts import render, redirect
from .forms import PriseVueForm, IndexeurForm, IndexationControlForm, PriseDeVueContentForm, IndexationControlContentForm, IndexeurContentForm
from datetime import datetime
from django.views import View
from django.db import connection
from django.contrib import messages
from Collecte.forms import SearchForm
# Create your views here.
def suivi(request):
    return render(request, 'suivi.html')
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
    
    # def dispatch(self, request, *args, **kwargs):
    #     # Vérification stricte + suppression immédiate de l'authentification
    #     if not request.session.get('indexeur_auth_token'):
    #         return redirect('indexeur_login')
        
    #     # Supprimer le token immédiatement après vérification
    #     token = request.session.pop('indexeur_auth_token', None)
    #     if not token:
    #         return redirect('indexeur_login')
            
    #     return super().dispatch(request, *args, **kwargs)
    def post(self, request):
        formIndexeur = IndexeurContentForm(request.POST)
        if formIndexeur.is_valid():
            try:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO indexeur (n_enregistrement, nomi) VALUES (%s, %s)",[formIndexeur.cleaned_data['n_enregistrement'], formIndexeur.cleaned_data['nomi']]
                    )
                    cursor.execute(
                        "UPDATE doc SET statut = 'suivi1' WHERE n_enregistrement = %s", [formIndexeur.cleaned_data['n_enregistrement']]
                    )
                messages.success(request, "Document affecté avec succès!")
                return redirect('indexeur_protected')
            except Exception as e:
                messages.error(request, f"Erreur lors de l'affectation du document: {str(e)}")

        return render(request, self.template_name, {'formIndexeur': formIndexeur})
    
    def get(self, request):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT i.nomi, COUNT(i.n_enregistrement) AS nombre
                FROM indexation i
                INNER JOIN doc d ON i.n_enregistrement = d.n_enregistrement
                WHERE d.statut = %s
                GROUP BY i.nomi
                ORDER BY i.nomi
            """, ['suivi1'])
            rows = cursor.fetchall()
            indexeurs = [
                {'nomi': row[0], 'nombre': row[1]}
                for row in rows
            ] if rows else []
        context = {
            'formIndexeur': IndexeurContentForm(),
            'formSearch': SearchForm(request.GET or None),
            'indexeurs': indexeurs,  # Toujours une liste
        }
        return render(request, self.template_name, context)
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
    

class PriseVueProtectedView(View):
    template_name = 'priseVue.html'
    
    # def dispatch(self, request, *args, **kwargs):
    #     # Vérification stricte + suppression immédiate de l'authentification
    #     if not request.session.get('priseVue_auth_token'):
    #         return redirect('priseVue_login')
        
    #     # Supprimer le token immédiatement après vérification
    #     token = request.session.pop('priseVue_auth_token', None)
    #     if not token:
    #         return redirect('priseVue_login')
            
    #     return super().dispatch(request, *args, **kwargs)
    def post(self, request):
        formPriseDeVueContentForm = PriseDeVueContentForm(request.POST)
        if formPriseDeVueContentForm.is_valid():
                try:
                    n_enregistrement = formPriseDeVueContentForm.cleaned_data['n_enregistrement']
                    # Récupérer nomi depuis la table indexeur
                    with connection.cursor() as cursor:
                        cursor.execute(
                            "UPDATE suivi SET dat_pv = %s, dat_rrsuivi = %s, dat_mont = %s, datsaisi_pv = %s WHERE n_enregistrement = %s",
                            [
                                datetime.today().strftime('%Y-%m-%d'),
                                formPriseDeVueContentForm.cleaned_data['dat_envoi_bibliotheque'],
                                datetime.today().strftime('%Y-%m-%d'),
                                datetime.today().strftime('%Y-%m-%d'),
                                n_enregistrement
                            ]
                        )
                        cursor.execute(
                            """SELECT nomc, dat_ctrl, visa FROM control WHERE n_enregistrement = %s,
                            """,
                            [
                                n_enregistrement 
                            ]
                        )
                        result = cursor.fetchone()
                        dat_ctrl = result[1] if result else None
                        nomc = result[0] if result else None
                        visa = result[2] if result else None
                        cursor.execute(
                                 """
                                 INSERT INTO vue (
                                     n_enregistrement, 
                                     dat_ctrl, 
                                     visa, 
                                     controleur,
                                     dat_recepv
                                     ) VALUES (%s, %s, %s, %s, %s)
                                 """, [
                                     n_enregistrement,
                                     dat_ctrl,
                                     visa,
                                     nomc,
                                     formPriseDeVueContentForm.cleaned_data['dat_recep_vue'],
                                 ]
                             )
                    
                        cursor.execute(
                            """
                            UPDATE doc SET statut = %s WHERE n_enregistrement
                            """,
                            [
                                "fini"
                            ]
                        )
                 
                    messages.success(request, "Document affecté avec succès!")
                    return redirect('priseVue_protected')
                except Exception as e:
                    messages.error(request, f"Erreur lors de l'affectation du document: {str(e)}")
        return render(request, self.template_name, {'formPriseDeVueContent': formPriseDeVueContentForm})
    def get(self, request):
        formSearch = SearchForm(request.GET or None)
        formPriseDeVueContentForm = PriseDeVueContentForm()
        
        context = {
            'formSearch': formSearch,
            'formPriseDeVueContent': formPriseDeVueContentForm,
        }
        return render(request, self.template_name, context)

class IndexationControlProtectedView(View):
    template_name = 'indexationControl.html'
    
    # def dispatch(self, request, *args, **kwargs):
    #     # Vérification stricte + suppression immédiate de l'authentification
    #     if not request.session.get('indexationControl_auth_token'):
    #         return redirect('indexationControl_login')
        
    #     # Supprimer le token immédiatement après vérification
    #     token = request.session.pop('indexationControl_auth_token', None)
    #     if not token:
    #         return redirect('indexationControl_login')
            
    #     return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        # Initialisation des formulaires
        formSearch = SearchForm(request.GET or None)
        formIndexationControlContent = IndexationControlContentForm()
        
        context = {
            'formSearch': formSearch,
            'formIndexationControlContent': formIndexationControlContent,
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        formIndexationControlContent = IndexationControlContentForm(request.POST)
        if formIndexationControlContent.is_valid():
                try:
                    n_enregistrement = formIndexationControlContent.cleaned_data['n_enregistrement']
                    # Récupérer nomi depuis la table indexeur
                    with connection.cursor() as cursor:
                        cursor.execute(
                            "SELECT nomi FROM indexeur WHERE n_enregistrement = %s", [n_enregistrement]
                        )
                        result = cursor.fetchone()
                        if not result:
                            messages.error(request, "Aucun indexeur trouvé pour ce document.")
                            return render(request, self.template_name, {'formIndexationControlContent': formIndexationControlContent})
                        nomi = result[0]
                        # Insérer dans indexation
                        cursor.execute(
                            "INSERT INTO indexation (n_enregistrement, nomi, dat_reception, dat_indexation, dat_saisi, dat_envoi) VALUES (%s, %s, %s, %s, %s, %s)",
                            [
                                n_enregistrement,
                                nomi,
                                formIndexationControlContent.cleaned_data['dat_recep_pour_indexation'],
                                datetime.today().strftime('%Y-%m-%d'),
                                datetime.today().strftime('%Y-%m-%d'),
                                formIndexationControlContent.cleaned_data['dat_envoi_control']
                            ]
                        )
                        cursor.execute(
                            """INSERT INTO control (
                                n_enregistrement, 
                                nomc, 
                                dat_ctrl, 
                                observation, 
                                retourne, 
                                dat_valid, 
                                dat_recepc) VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                            [
                                n_enregistrement,
                                formIndexationControlContent.cleaned_data['nomc'],
                                datetime.today().strftime('%Y-%m-%d'),
                                formIndexationControlContent.cleaned_data['observation'],
                                'Non',
                                 # Partie enlever du formulaire
                                # formIndexationControl.cleaned_data['dat_retour_correc'],
                                datetime.today().strftime('%Y-%m-%d'),
                                formIndexationControlContent.cleaned_data['dat_recep_pour_controle'],
                            ]
                        )
                        cursor.execute(
                                 "SELECT dat_rsuivi FROM controle WHERE n_enregistrement = %s",
                                 [n_enregistrement]
                             )
                        result = cursor.fetchone()
                        dat_rsuivi = result[0] if result else None
                        cursor.execute(
                            "UPDATE suivi SET noms = %s, datsaisi_ic = %s, dat_rsuivi = %s WHERE n_enregistrement = %s",
                            [
                                formIndexationControlContent.cleaned_data['noms'],
                                formIndexationControlContent.cleaned_data['dat_envoi_suivi'],
                                n_enregistrement
                            ]
                        )
                        cursor.execute(
                            """
                            UPDATE doc SET statut = %s WHERE n_enregistrement
                            """,
                            [
                                "suivi2"
                            ]
                        )
                 
                    messages.success(request, "Document affecté avec succès!")
                    return redirect('indexationControl_protected')
                except Exception as e:
                    messages.error(request, f"Erreur lors de l'affectation du document: {str(e)}")
        return render(request, self.template_name, {'formIndexationControlContent': formIndexationControlContent})
    
def priseVue_logout(request):
    request.session.flush()
    return redirect('priseVue_login')

def indexeur_logout(request):
    request.session.flush()
    return redirect('indexeur_login')

def indexationControl_logout(request):
    request.session.flush()
    return redirect('indexationControl_login')