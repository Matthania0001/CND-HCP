from django import forms
from datetime import datetime
from Main.models import Doc
class ArchivageDocForm(forms.Form):
    num = forms.ChoiceField(
        label="N° d'enregistrement",
        choices = [(num.n_enregistrement, num.n_enregistrement) for num in Doc.objects.all()],
        widget=forms.Select(attrs={'class': 'form-input'}),
    )
    
    dat_saisie = forms.DateField(
        label="Date de Saisie",
        input_formats=['%Y-%m-%d'],
        help_text="Format: AAAA-MM-JJ",
        initial=datetime.today().date(),
        widget=forms.DateInput(attrs={'class': 'form-input'})
    
     )
    
    dat_envoi = forms.DateField(
        label="Date d'envoi à l'archivage",
        input_formats=['%Y-%m-%d'],
        help_text="Format: AAAA-MM-JJ",
        widget=forms.DateInput(attrs={'class': 'form-input'})
    
     )