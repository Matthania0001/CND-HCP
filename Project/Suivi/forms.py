from django import forms
from Main.models import Doc
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

class PriseVueForm(BaseCollecteForm):
    pass

class IndexeurForm(BaseCollecteForm):
    pass

class IndexationControlForm(BaseCollecteForm):
    pass

    
class PriseDeVueContentForm(forms.Form):
    num = forms.ChoiceField(
        label="N° d'enregistrement",
        choices = [(num.n_enregistrement, num.n_enregistrement) for num in Doc.objects.all()],
        widget=forms.Select(attrs={'class': 'form-input'})
    )
    dat_recep_vue = forms.DateField(
        label="Date de reception à la Numérisation",
        input_formats=['%Y-%m-%d'],
        help_text="Format: AAAA-MM-JJ",
        widget=forms.DateInput(attrs={'class': 'form-input'})
    )
    dat_envoi_bibliotheque = forms.DateField(
        label="Date de Sortie à la Numérisation",
        input_formats=['%Y-%m-%d'],
        help_text="Format: AAAA-MM-JJ",
        widget=forms.DateInput(attrs={'class': 'form-input'})
    )

class IndexeurContentForm(forms.Form):
    num = forms.ChoiceField(
        label="N° d'enregistrement",
        choices = [(num.n_enregistrement, num.n_enregistrement) for num in Doc.objects.all()],
        widget=forms.Select(attrs={'class': 'form-input'})
    )

    nomi = forms.CharField(
        label="Nom de l'indexeur",
        max_length=100,
        widget=forms.TextInput(attrs={'size': '50', 'class': 'form-input'}),
        help_text="Nom de l'indexeur qui a effectué la saisie"
    )
    
    
class IndexationControlContentForm(forms.Form):
    num = forms.ChoiceField(
        label="N° d'enregistrement",
        choices = [(num.n_enregistrement, num.n_enregistrement) for num in Doc.objects.all()],
        widget=forms.Select(attrs={'class': 'form-input'})
    )
    dat_recep_pour_indexation = forms.DateField(
        label="Date de réception",
        input_formats=['%Y-%m-%d'],
        help_text="Format: AAAA-MM-JJ",
        widget=forms.DateInput(attrs={'class': 'form-input'})
    )
    dat_envoi_control = forms.DateField(
        label="Date d'envoi au contrôle",
        input_formats=['%Y-%m-%d'],
        help_text="Format: AAAA-MM-JJ",
        widget=forms.DateInput(attrs={'class': 'form-input'})
    )
    dat_recep_pour_controle = forms.DateField(
        label="Date de réception pour controle",
        input_formats=['%Y-%m-%d'],
        help_text="Format: AAAA-MM-JJ",
        widget=forms.DateInput(attrs={'class': 'form-input'})
    )
    observation = forms.CharField(
        label="Observation du contrôleur",
        widget=forms.Textarea(attrs={
            'rows': 3,
            'cols': 50,
            'class': 'form-input'
        }),
        help_text="Notes et remarques du contrôleur",
    )
    nomc = forms.CharField(
        label="Nom du controleur",
        max_length=100,
        widget=forms.TextInput(attrs={'size': '50', 'class': 'form-input'}),
    )
    dat_envoi_suivi = forms.DateField(
        label="Date d'envoi au suivi",
        input_formats=['%Y-%m-%d'],
        help_text="Format: AAAA-MM-JJ",
        widget=forms.DateInput(attrs={'class': 'form-input'})
    )
    noms = forms.CharField(
        label="Nom du responsable de suivi",
        max_length=100,
        widget=forms.TextInput(attrs={'size': '50', 'class': 'form-input'}),
    )
    dat_envoi_bibliotheque = forms.DateField(
        label="Date d'envoi à la bibliothèque ou à la source expeditrice",
        input_formats=['%Y-%m-%d'],
        help_text="Format: AAAA-MM-JJ",
        widget=forms.DateInput(attrs={'class': 'form-input'})
    )