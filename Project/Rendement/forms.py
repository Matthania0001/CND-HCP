from django import forms
from Main.models import Indexeur
class CompareSearchForm(forms.Form):
    # Date fields
    date = forms.BooleanField(
        required=False,
        initial=False,
        label='Période',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )
    de = forms.DateField(
        required=False,
        input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(attrs={
            'size': '10',
            'class': 'form-input',
            'placeholder': 'AAAA-MM-JJ'
        }),
        label='De',
        help_text= "Date de début"
    )
    a = forms.DateField(
        required=False,
        input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(attrs={
            'size': '10',
            'class': 'form-input',
            'placeholder': 'AAAA-MM-JJ'
        }),
        label='À',
        help_text= "Date de fin"
    )
    
    # Domain field
    nomi = forms.BooleanField(
        required=False, 
        initial=False, 
        label='Nom de l\'indexeur',  
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    nomIndexeur = forms.ChoiceField(
        required=False,
        choices=[(indexeur.nomi,indexeur.nomi) for indexeur in Indexeur.objects.all() ],  # You'll need to populate this with your domain choices
        widget=forms.Select(attrs={'class': 'form-input'}),
        help_text= 'Selectionner l\'indexeur'
    )
    