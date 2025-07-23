from django import forms
from django.db import models
from Main.models import Domaine, Source, Doc, Depot
class DocumentSearchForm(forms.Form):
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
    domain = forms.BooleanField(
        required=False, 
        initial=False, 
        label='Domaine',  
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    domaine = forms.ChoiceField(
        required=False,
        choices=[(domaine.domaine,domaine.domaine) for domaine in Domaine.objects.all() ],  # You'll need to populate this with your domain choices
        widget=forms.Select(attrs={'class': 'form-input'}),
        help_text= 'Selectionner un domaine'
    )
    
    # Source field
    src = forms.BooleanField(
        required=False, 
        initial=False, 
        label='Source',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
        )
    source = forms.ChoiceField(
        required=False,
        choices=[(source.source,source.source) for source in Source.objects.all() ],  # You'll need to populate this with your domain choices
        widget=forms.Select(attrs={'class': 'form-input'}),
        help_text= 'Selectionner une source'
    )
    
    # Status field
    stat = forms.BooleanField(
        required=False, 
        initial=False, 
        label='Statut',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
        )
    statut = forms.ChoiceField(
        required=False,
        choices=[(statut['statut'], statut['statut']) for statut in Doc.objects.values('statut').distinct()],  # You'll need to populate this with your domain choices
        widget=forms.Select(attrs={'class': 'form-input'}),
        help_text= 'Selectionner un statut'
    )
    
    
    
class EtsSearchForm(forms.Form):
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
    type = forms.BooleanField(
        required=False, 
        initial=False, 
        label='Type de dépot',  
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    type_depot = forms.ChoiceField(
        required=False,
        choices=[(depot.type,depot.type) for depot in Depot.objects.all() ],  # You'll need to populate this with your domain choices
        widget=forms.Select(attrs={'class': 'form-input'}),
        help_text= 'Selectionner un type de dépot'
    )
    