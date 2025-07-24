from django import forms
from Main.models import Source, Domaine, Doc
class BaseCollecteForm(forms.Form):
    username = forms.CharField(
        label="Login",
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
        }),
        required=True
    )

class SourceLoginForm(BaseCollecteForm):
    pass

class DomaineLoginForm(BaseCollecteForm):
    pass

class SourceSuppressionForm(forms.Form):
    source = forms.ChoiceField(
        label="Source à supprimer",
        choices = [(source.source, source.source) for source in Source.objects.all()],
        widget=forms.Select(attrs={'class': 'form-input'}),
        help_text = "Sélectionner la source à supprimer.",
        required=False
    )
class SourceAjoutForm(forms.Form):
    nom_source = forms.CharField(
        label="Nom de la source à ajouter",
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-input'}),
        help_text="Entrer le nom de la source à ajouter.",
        required=False
    )

class DomaineSuppressionForm(forms.Form):
    domaine = forms.ChoiceField(
        label="Domaine à supprimer",
        choices = [(domaine.domaine, domaine.domaine) for domaine in Domaine.objects.all()],
        widget=forms.Select(attrs={'class': 'form-input'}),
        help_text = "Sélectionner le domaine à supprimer.",
        required=False
    )
class DomaineAjoutForm(forms.Form):
    nom_domaine = forms.CharField(
        label="Nom du domaine à ajouter",
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-input'}),
        help_text="Entrer le nom du domaine à ajouter.",
        required=False
    )
    
# class DocTypeSearchForm(forms.Form):
#     # Date fields
#     date = forms.BooleanField(
#         required=False,
#         initial=False,
#         label='Période',
#         widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
#     )
#     de = forms.DateField(
#         required=False,
#         input_formats=['%Y-%m-%d'],
#         widget=forms.DateInput(attrs={
#             'size': '10',
#             'class': 'form-input',
#             'placeholder': 'AAAA-MM-JJ'
#         }),
#         label='De',
#         help_text= "Date de début"
#     )
#     a = forms.DateField(
#         required=False,
#         input_formats=['%Y-%m-%d'],
#         widget=forms.DateInput(attrs={
#             'size': '10',
#             'class': 'form-input',
#             'placeholder': 'AAAA-MM-JJ'
#         }),
#         label='À',
#         help_text= "Date de fin"
#     )
    
#     # Domain field
#     type = forms.BooleanField(
#         required=False, 
#         initial=False, 
#         label='Type de périodicité',  
#         widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
#     type_doc = forms.ChoiceField(
#         label='Type de Périodicité',
#         required=False,
#         choices=[('np', 'Non Périodique'), ('p', 'Périodique')],  # You'll need to populate this with your domain choices
#         widget=forms.Select(attrs={'class': 'form-input'}),
#         help_text= 'Selectionner le type de périodicité'
#     )
    
#     lg = forms.BooleanField(
#         required=False, 
#         initial=False, 
#         label='Langue',  
#         widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
#     langue_doc = forms.ChoiceField(
#         label='Langue du document',
#         required=False,
#         choices=[('Ar', 'Arabe'), ('Fr', 'France'), ('En', 'Anglais')],  # You'll need to populate this with your domain choices
#         widget=forms.Select(attrs={'class': 'form-input'}),
#         help_text= 'Selectionner la langue du document'
#     )
    

class SearchByNumberForm(forms.Form):
    num = forms.ChoiceField(
        label="Numéro de document",
        choices=[(doc.n_enregistrement, doc.n_enregistrement) for doc in Doc.objects.all()],
        widget=forms.Select(attrs={'class': 'form-input'}),
        )