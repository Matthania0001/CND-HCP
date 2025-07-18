CREATE TABLE admin (
  id TINYINT UNSIGNED NOT NULL AUTO_INCREMENT,
  nom VARCHAR(50) NOT NULL,
  email VARCHAR(75) NOT NULL,
  login VARCHAR(20) NOT NULL,
  pass VARCHAR(32) NOT NULL,
  destination VARCHAR(30) NOT NULL,
  PRIMARY KEY (id)
) ENGINE=MyISAM
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_general_ci;

CREATE TABLE auteur (
  id SMALLINT NOT NULL,
  auteur VARCHAR(200) NOT NULL,
  PRIMARY KEY (id),
  KEY idx_auteur (auteur)
) ENGINE=MyISAM
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_general_ci;


CREATE TABLE collecte (
  nomrc VARCHAR(100) NOT NULL,
  n_enregistrement SMALLINT NOT NULL,
  datsaisi_c DATE NOT NULL,
  PRIMARY KEY (nomrc, n_enregistrement)
) ENGINE=MyISAM
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_general_ci;

# Enlever la contrainte clé primaire de la table collecte et ajouter un id qui sera clé primaire
#ensuite ajouter une contrainte unique pour nomrc et n_enregistrement
#ADD UNIQUE KEY uniq_collecte_nomrc_nenregistrement (nomrc, n_enregistrement);
#ADD COLUMN id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST;
CREATE TABLE collecteur (
  nomrc VARCHAR(100) NOT NULL,
  PRIMARY KEY (nomrc)
) ENGINE=MyISAM
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_general_ci;

CREATE TABLE control (
  nomc VARCHAR(100) NOT NULL,
  dat_ctrl DATE NOT NULL,
  observation VARCHAR(200) DEFAULT NULL,
  retourne CHAR(3) NOT NULL,
  dat_retour DATE DEFAULT NULL,
  dat_valid DATE NOT NULL,
  visa VARCHAR(50) NOT NULL,
  n_enregistrement SMALLINT NOT NULL,
  dat_recepc DATE NOT NULL,
  PRIMARY KEY (nomc, n_enregistrement)
) ENGINE=MyISAM
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_general_ci;

#DROP PRIMARY KEY;
#ADD COLUMN id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST;
#ADD UNIQUE KEY uniq_collecte_nomc_nenregistrement (nomc, n_enregistrement);

CREATE TABLE controleur (
  nomc VARCHAR(100) NOT NULL,
  PRIMARY KEY (nomc)
) ENGINE=MyISAM
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_general_ci;

CREATE TABLE controleurpv (
  controleur VARCHAR(100) NOT NULL,
  PRIMARY KEY (controleur)
) ENGINE=MyISAM
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_general_ci;

CREATE TABLE depot (
  type VARCHAR(30) NOT NULL,
  PRIMARY KEY (type)
) ENGINE=MyISAM
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_general_ci;

CREATE TABLE doc (
  n_enregistrement BIGINT UNSIGNED NOT NULL,
  titre VARCHAR(200) NOT NULL,
  titre_article VARCHAR(200) DEFAULT NULL,
  pages VARCHAR(30) DEFAULT '0',
  domaine VARCHAR(80) NOT NULL,
  type VARCHAR(100) NOT NULL,
  periodicite CHAR(3) DEFAULT '0',
  vol VARCHAR(25) NOT NULL,
  tom VARCHAR(25) NOT NULL,
  num VARCHAR(25) NOT NULL,
  statut VARCHAR(10) NOT NULL DEFAULT '0',
  n_periodique SMALLINT DEFAULT NULL,
  lang CHAR(2) NOT NULL,
  PRIMARY KEY (n_enregistrement),
  KEY idx_titre (titre)
) ENGINE=MyISAM
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_general_ci;

CREATE TABLE domaine (
  domaine VARCHAR(100) NOT NULL,
  PRIMARY KEY (domaine)
) ENGINE=MyISAM
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_general_ci;

CREATE TABLE ecriture (
  auteur VARCHAR(255) NOT NULL,
  n_enregistrement SMALLINT NOT NULL,
  PRIMARY KEY (auteur(191), n_enregistrement)
) ENGINE=MyISAM
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_general_ci;

#DROP PRIMARY KEY;
#ADD COLUMN id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST;
#ADD UNIQUE KEY uniq_auteur_nenregistrement (auteur, n_enregistrement);

CREATE TABLE editeur (
  editeur VARCHAR(200) NOT NULL,
  PRIMARY KEY (editeur)
) ENGINE=MyISAM
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_general_ci;

CREATE TABLE edition (
  editeur VARCHAR(255) NOT NULL,
  n_enregistrement SMALLINT NOT NULL,
  date_edition DATE NOT NULL,
  ville_edition VARCHAR(60) DEFAULT NULL,
  PRIMARY KEY (editeur(191), n_enregistrement)
) ENGINE=MyISAM
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_general_ci;

#DROP PRIMARY KEY;
#ADD COLUMN id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST;
#ADD UNIQUE KEY uniq_editeur_nenregistrement (editeur, n_enregistrement);

CREATE TABLE fournit (
  source VARCHAR(255) NOT NULL,
  n_enregistrement SMALLINT NOT NULL,
  date_reception DATE NOT NULL,
  obligation VARCHAR(30) NOT NULL,
  PRIMARY KEY (source(191), n_enregistrement)
) ENGINE=MyISAM
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_general_ci;

#DROP PRIMARY KEY;
#ADD COLUMN id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST;
#ADD UNIQUE KEY uniq_source_nenregistrement (source, n_enregistrement);

CREATE TABLE indexation (
  nomi VARCHAR(100) NOT NULL,
  n_enregistrement SMALLINT NOT NULL,
  dat_reception DATE NOT NULL,
  dat_indexation DATE NOT NULL,
  dat_saisi DATE NOT NULL,
  dat_envoi DATE NOT NULL,
  PRIMARY KEY (nomi, n_enregistrement)
) ENGINE=MyISAM
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_general_ci;

#DROP PRIMARY KEY;
#ADD COLUMN id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST;
#ADD UNIQUE KEY uniq_nomi_nenregistrement (nomi, n_enregistrement);

CREATE TABLE indexeur (
  nomi VARCHAR(100) NOT NULL,
  PRIMARY KEY (nomi)
) ENGINE=MyISAM
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_general_ci;

CREATE TABLE source (
  source VARCHAR(200) NOT NULL,
  PRIMARY KEY (source)
) ENGINE=MyISAM
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_general_ci;

CREATE TABLE suiveur (
  noms VARCHAR(100) NOT NULL,
  PRIMARY KEY (noms)
) ENGINE=MyISAM
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_general_ci;

CREATE TABLE suivi (
  noms VARCHAR(100) NOT NULL,
  n_enregistrement SMALLINT NOT NULL,
  datenvoi_t DATE NOT NULL,
  dat_rsuivi DATE NOT NULL,
  datsaisi_ic DATE NOT NULL,
  datenvoi_sir DATE NOT NULL,
  dat_pv DATE NOT NULL,
  dat_mont DATE NOT NULL,
  dat_rrsuivi DATE NOT NULL,
  datsaisi_pv DATE NOT NULL,
  PRIMARY KEY (noms, n_enregistrement)
) ENGINE=MyISAM
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_general_ci;

#DROP PRIMARY KEY,
#ADD COLUMN id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST,
#ADD UNIQUE KEY uniq_noms_nenregistrement (noms, n_enregistrement);

CREATE TABLE vue (
  controleur VARCHAR(100) NOT NULL,
  n_enregistrement SMALLINT NOT NULL,
  dat_ctrl DATE NOT NULL,
  visa VARCHAR(50) NOT NULL,
  dat_recepv DATE NOT NULL,
  PRIMARY KEY (controleur, n_enregistrement)
) ENGINE=MyISAM
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_general_ci;

#DROP PRIMARY KEY,
#ADD COLUMN id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST,
#ADD UNIQUE KEY uniq_controleur_nenregistrement (controleur, n_enregistrement);


