from django.test import TestCase
from .forms import IndexationControlContentForm

class IndexationControlContentFormTest(TestCase):
    def test_form_validation(self):
        # Test avec des données valides
        valid_data = {
            'dat_envoi_suivi': '2023-01-01',
            'observation': 'Test observation'
        }
        form = IndexationControlContentForm(data=valid_data)
        self.assertTrue(form.is_valid())
        
        # Test avec des données invalides
        invalid_data = {
            'dat_envoi_suivi': '',  # Champ requis vide
            'observation': ''       # Champ requis vide
        }
        form = IndexationControlContentForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        print(form.errors)  # Affiche toutes les erreurs
        # Ou pour des champs spécifiques
        print(form['dat_envoi_suivi'].errors)
        print(form['observation'].errors)
