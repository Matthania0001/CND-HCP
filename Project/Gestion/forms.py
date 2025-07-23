from django import forms
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
