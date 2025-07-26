from django.db import models

# Create your models here.
from django.db import models

class Personne(models.Model):
    n_enregistrement = models.CharField(max_length=50)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    age = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.nom} {self.prenom}"