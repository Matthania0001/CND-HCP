from django import forms
from .models import Personne

class PremierFormulaire(forms.ModelForm):
    class Meta:
        model = Personne
        fields = ['n_enregistrement', 'nom', 'prenom']
        
class DeuxiemeFormulaire(forms.ModelForm):
    class Meta:
        model = Personne
        fields = ['n_enregistrement', 'nom', 'prenom', 'age']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Rendre les champs communs en lecture seule
        self.fields['n_enregistrement'].widget.attrs['readonly'] = True
        self.fields['nom'].widget.attrs['readonly'] = True
        self.fields['prenom'].widget.attrs['readonly'] = True