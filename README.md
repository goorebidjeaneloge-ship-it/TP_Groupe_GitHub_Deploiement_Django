# Gestion de stock

Application web de gestion de stock réalisée avec Django dans le cadre du TP collaboratif GitHub et déploiement Django.

> **État du projet :** ce README présente le périmètre demandé. Les commandes, fonctionnalités, versions et URL de déploiement devront être confirmées
> avec le code final du groupe.

## Objectif

Gérer des produits classés par catégorie et repérer ceux dont le stock passe sous leur seuil d’alerte.

## Fonctionnalités demandées

- Créer, consulter, modifier et supprimer des produits.
- Associer chaque produit à une catégorie.
- Filtrer les produits par catégorie.
- Signaler les produits dont la quantité est inférieure au seuil d’alerte.
- Administrer les données depuis Django Admin, si cette fonctionnalité est activée dans le projet.

## Modèles prévus

- **Categorie** : nom et autres champs retenus par l’équipe.
- **Produit** : nom, quantité, seuil d’alerte et catégorie associée.

Les noms des champs ci-dessus sont à harmoniser avec les modèles réellement implémentés.

## Prérequis

- Python 3
- pip
- Git

La version de Python et celle de Django utilisées par le projet seront précisées après vérification de `requirements.txt`.

## Installation locale

```bash
git clone https://github.com/goorebidjeaneloge-ship-it/TP_Groupe_GitHub_Deploiement_Django.git
cd TP_Groupe_GitHub_Deploiement_Django
python -m venv venv
```

Activer l’environnement virtuel :

**Windows PowerShell**

```powershell
.\venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
source venv/bin/activate
```

Installer les dépendances et préparer la base de données :

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Puis ouvrir http://127.0.0.1:8000/ dans le navigateur.

> Si le dépôt ne contient pas encore `requirements.txt` ou si le point d’entrée Django n’est pas à la racine, ces commandes devront être ajustées.

## Tests

Lorsque les tests auront été ajoutés au projet, les lancer avec :

```bash
python manage.py test
```

Parcours à vérifier : création d’un produit, affichage de la liste, filtre par catégorie, modification, suppression et alerte lorsque `quantité < seuil_alerte`. Une quantité égale au seuil ne devrait pas déclencher l’alerte, puisque la règle demandée est « inférieur au seuil ».

## Équipe et contributions

| Membre | Responsabilité prévue | Branche / Pull Request |
|---|---|---|
| Djean-bi Goore  | Coordination, dépôt et intégration | À compléter |
| Onikoyamou Moïse  | Modèles, ORM, migrations et administration | À compléter |
| Kouakou Christ Evrard| Vues, URLs et logique métier | À compléter |
| Kone Mohamed Dia| Templates et formulaires | À compléter |
| Kouassi Mihinsa Jean-Loïs| Tests, README et déploiement | 


## Déploiement

- **Hébergeur :** à confirmer
- **URL publique :** à ajouter après le déploiement
- Les paramètres sensibles, notamment `SECRET_KEY`, doivent être fournis par variables d’environnement et ne doivent pas être commités.
- En production, configurer notamment `DEBUG=False`, `ALLOWED_HOSTS`, les fichiers statiques et la base de données selon l’hébergeur.

## Dépôt

https://github.com/goorebidjeaneloge-ship-it/TP_Groupe_GitHub_Deploiement_Django
