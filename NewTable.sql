CREATE TABLE doc_monographie (
  n_enregistrement bigint(20) unsigned NOT NULL,
  titre varchar(200) NOT NULL,
  pages varchar(30) DEFAULT '0',
  domaine varchar(80) NOT NULL,
  type varchar(100) NOT NULL,
  statut varchar(10) NOT NULL DEFAULT '0',
  n_periodique smallint(6) DEFAULT NULL,
  lang char(2) NOT NULL,
  type_support varchar(255) DEFAULT NULL,
  acces varchar(255) DEFAULT NULL,
  id_acces_arabe varchar(255) DEFAULT NULL,
  id_acces_etranger varchar(255) DEFAULT NULL,
  PRIMARY KEY (n_enregistrement),
  KEY idx_titre (titre)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE doc_article (
  n_enregistrement bigint(20) unsigned NOT NULL,
  titre varchar(200) NOT NULL,
  titre_article varchar(200) DEFAULT NULL,
  pages varchar(30) DEFAULT '0',
  domaine varchar(80) NOT NULL,
  type varchar(100) NOT NULL,
  periodicite char(3) DEFAULT '0',
  vol varchar(25) NOT NULL,
  tom varchar(25) NOT NULL,
  num varchar(25) NOT NULL,
  statut varchar(10) NOT NULL DEFAULT '0',
  n_periodique smallint(6) DEFAULT NULL,
  lang char(2) NOT NULL,
  type_support varchar(255) DEFAULT NULL,
  acces varchar(255) DEFAULT NULL,
  id_acces_etranger varchar(255) DEFAULT NULL,
  id_acces_arabe varchar(255) DEFAULT NULL,
  PRIMARY KEY (n_enregistrement),
  KEY idx_titre (titre)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE doc_collecte (
  n_enregistrement bigint(20) unsigned NOT NULL,
  titre_document varchar(200) NOT NULL,
  source_document varchar(100) NOT NULL,
  support_document varchar(50) NOT NULL,
  date_collecte date NOT NULL,
  statut varchar(255) DEFAULT NULL,
  PRIMARY KEY (n_enregistrement)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE auteur (
  auteur varchar(200) NOT NULL,
  n_enregistrement bigint(20) DEFAULT NULL,
  KEY idx_auteur (auteur)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE editeur (
  editeur varchar(200) NOT NULL,
  ville_edition varchar(100) DEFAULT NULL,
  n_enregistrement bigint(20) DEFAULT NULL,
  date_edition date DEFAULT NULL,
  PRIMARY KEY (editeur)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE doc_enregistre (
  n_enregistrement bigint(20) unsigned NOT NULL,
  statut varchar(255) NOT NULL,
  responsable_saisie varchar(255) NOT NULL,
  date_saisie date NOT NULL,
  PRIMARY KEY (n_enregistrement)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

DROP TABLE auteur;
DROP TABLE editeur;