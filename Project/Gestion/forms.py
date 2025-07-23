from django import forms
from Main.models import Source, Domaine
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