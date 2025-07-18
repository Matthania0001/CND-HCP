
from django.db import models


class Admin(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    nom = models.CharField(max_length=50, null  = False, default = '')
    email = models.CharField(max_length=75, null  = False, default = '')
    login = models.CharField(max_length=20, null  = False, default = '')
    pass_field = models.CharField(db_column='pass', max_length=32, null  = False, default = '')  # Field renamed because it was a Python reserved word.
    destination = models.CharField(max_length=30, null  = False, default = '')

    class Meta:
        managed = False
        db_table = 'admin'


class Auteur(models.Model):
    id = models.SmallIntegerField(primary_key = True, null = False)
    auteur = models.CharField(max_length=200, null = False, default = '0')

    class Meta:
        managed = False
        db_table = 'auteur'
        indexes = [
            models.Index(fields=['auteur'], name='idx_auteur'),  # index nommé sur le champ 'champ'
        ]


class Collecte(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    nomrc = models.CharField(max_length=100, null = False, default = '')  # The composite primary key (nomrc, n_enregistrement) found, that is not supported. The first column is selected.
    n_enregistrement = models.SmallIntegerField(null = False, default = '0')
    datsaisi_c = models.DateField(null = False, default = '0000-00-00')

    class Meta:
        managed = False
        db_table = 'collecte'
        unique_together = (('nomrc', 'n_enregistrement'),)


class Collecteur(models.Model):
    nomrc = models.CharField(max_length=100, primary_key = True)

    class Meta:
        managed = False
        db_table = 'collecteur'


class Control(models.Model): 
    id = models.PositiveIntegerField(primary_key=True)
    nomc = models.CharField(max_length=100, null = False, default = '')  # The composite primary key (nomc, n_enregistrement) found, that is not supported. The first column is selected.
    dat_ctrl = models.DateField(null = False, default = '0000-00-00')
    observation = models.CharField(max_length=200, blank=True, null=True)
    retourne = models.CharField(max_length=3, null = False, default = '')
    dat_retour = models.DateField(blank=True, null=True)
    dat_valid = models.DateField(null = False,default = '0000-00-00')
    visa = models.CharField(max_length=50, null = False, default = '')
    n_enregistrement = models.SmallIntegerField(null = False, default = '0')
    dat_recepc = models.DateField(null = False, default = '0000-00-00')

    class Meta:
        managed = False
        db_table = 'control'
        unique_together = (('nomc', 'n_enregistrement'),)


class Controleur(models.Model):
    nomc = models.CharField(max_length=100, primary_key = True, null = False)

    class Meta:
        managed = False
        db_table = 'controleur'


class Controleurpv(models.Model):
    controleur = models.CharField(max_length=100, null = False, primary_key = True)

    class Meta:
        managed = False
        db_table = 'controleurpv'


class Depot(models.Model):
    type = models.CharField(primary_key=True, max_length=30, null = False)

    class Meta:
        managed = False
        db_table = 'depot'


class Doc(models.Model):
    n_enregistrement = models.PositiveBigIntegerField(primary_key = True)
    titre = models.CharField(max_length=200, null = False)
    titre_article = models.CharField(max_length=200, blank=True, null=True)
    pages = models.CharField(max_length=30, blank=True, null=True)
    domaine = models.CharField(max_length=80, null = False)
    type = models.CharField(max_length=100 , null = False)
    periodicite = models.CharField(max_length=3, default = '0')
    vol = models.CharField(max_length=25, null = False)
    tom = models.CharField(max_length=25, null = False)
    num = models.CharField(max_length=25, null = False)
    statut = models.CharField(max_length=10, null = False, default = '0')
    n_periodique = models.SmallIntegerField(blank=True, null=True)
    lang = models.CharField(max_length=2, null = False)

    class Meta:
        managed = False
        db_table = 'doc'
        indexes = [
            models.Index(fields=['titre'], name='idx_titre'),
        ]


class Domaine(models.Model):
    domaine = models.CharField(max_length=100, null = False, primary_key = True)

    class Meta:
        managed = False
        db_table = 'domaine'


class Ecriture(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    auteur = models.CharField(max_length=255, null = False, default = '0')  # The composite primary key (auteur, n_enregistrement) found, that is not supported. The first column is selected.
    n_enregistrement = models.SmallIntegerField(null = False, default = '0')

    class Meta:
        managed = False
        db_table = 'ecriture'
        unique_together = (('auteur', 'n_enregistrement'),)


class Editeur(models.Model):
    editeur = models.CharField(max_length=200, null = False, primary_key = True)

    class Meta:
        managed = False
        db_table = 'editeur'


class Edition(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    editeur = models.CharField(max_length=255, null = False, default = '0')  # The composite primary key (editeur, n_enregistrement) found, that is not supported. The first column is selected.
    n_enregistrement = models.SmallIntegerField(null = False, default = '0')
    date_edition = models.DateField(null = False, default = '0000-00-00')
    ville_edition = models.CharField(max_length=60, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'edition'
        unique_together = (('editeur', 'n_enregistrement'),)


class Fournit(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    source = models.CharField(max_length=255, default = '0')  # The composite primary key (source, n_enregistrement) found, that is not supported. The first column is selected.
    n_enregistrement = models.SmallIntegerField(default = '0')
    date_reception = models.DateField(default = '0000-00-00')
    obligation = models.CharField(max_length=30, default = '')

    class Meta:
        managed = False
        db_table = 'fournit'
        unique_together = (('source', 'n_enregistrement'),)


class Indexation(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    nomi = models.CharField(max_length=100, null = False, default = '')  # The composite primary key (nomi, n_enregistrement) found, that is not supported. The first column is selected.
    n_enregistrement = models.SmallIntegerField(null = False, default = '0')
    dat_reception = models.DateField(null = False, default = '0000-00-00')
    dat_indexation = models.DateField(null = False, default = '0000-00-00')
    dat_saisi = models.DateField(null = False, default = '0000-00-00')
    dat_envoi = models.DateField(null = False, default = '0000-00-00')

    class Meta:
        managed = False
        db_table = 'indexation'
        unique_together = (('nomi', 'n_enregistrement'),)


class Indexeur(models.Model):
    nomi = models.CharField(max_length=100, null = False,primary_key = True)

    class Meta:
        managed = False
        db_table = 'indexeur'


class Source(models.Model):
    source = models.CharField(max_length=200, null = False, primary_key = True)

    class Meta:
        managed = False
        db_table = 'source'


class Suiveur(models.Model):
    noms = models.CharField(max_length=100, null = False, primary_key = True)

    class Meta:
        managed = False
        db_table = 'suiveur'


class Suivi(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    noms = models.CharField(max_length=100, null = False, default = '')  # The composite primary key (noms, n_enregistrement) found, that is not supported. The first column is selected.
    n_enregistrement = models.SmallIntegerField(null = False, default = '0')
    datenvoi_t = models.DateField(null = False, default = '0000-00-00')
    dat_rsuivi = models.DateField(null = False, default = '0000-00-00')
    datsaisi_ic = models.DateField(null = False, default = '0000-00-00')
    datenvoi_sir = models.DateField(null = False, default = '0000-00-00')
    dat_pv = models.DateField(null = False, default = '0000-00-00')
    dat_mont = models.DateField(null = False, default = '0000-00-00')
    dat_rrsuivi = models.DateField(null = False, default = '0000-00-00')
    datsaisi_pv = models.DateField(null = False, default = '0000-00-00')

    class Meta:
        managed = False
        db_table = 'suivi'
        unique_together = (('noms', 'n_enregistrement'),)


class Vue(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    controleur = models.CharField(max_length=100, default = '')  # The composite primary key (controleur, n_enregistrement) found, that is not supported. The first column is selected.
    n_enregistrement = models.SmallIntegerField(default = '0')
    dat_ctrl = models.DateField(default = '0000-00-00')
    visa = models.CharField(max_length=50, default = '')
    dat_recepv = models.DateField(default = '0000-00-00')

    class Meta:
        managed = False
        db_table = 'vue'
        unique_together = (('controleur', 'n_enregistrement'),)
