from django import forms

class DocTypeSearchForm(forms.Form):
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
        label='Type de périodicité',  
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    type_doc = forms.ChoiceField(
        label='Type de Périodicité',
        required=False,
        choices=[('np', 'Non Périodique'), ('p', 'Périodique')],  # You'll need to populate this with your domain choices
        widget=forms.Select(attrs={'class': 'form-input'}),
        help_text= 'Selectionner le type de périodicité'
    )
    
    lg = forms.BooleanField(
        required=False, 
        initial=False, 
        label='Langue',  
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    langue_doc = forms.ChoiceField(
        label='Langue du document',
        required=False,
        choices=[('Ar', 'Arabe'), ('Fr', 'France'), ('En', 'Anglais')],  # You'll need to populate this with your domain choices
        widget=forms.Select(attrs={'class': 'form-input'}),
        help_text= 'Selectionner la langue du document'
    )


