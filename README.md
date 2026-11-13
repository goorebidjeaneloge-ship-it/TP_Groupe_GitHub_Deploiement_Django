# Gestion de stock — TP Django / GitHub / Déploiement

Application web Django de gestion de stock : catégories de produits, CRUD complet, filtre par
catégorie et signalement automatique des produits dont le stock est **inférieur** au seuil d'alerte.

- **Dépôt :** https://github.com/goorebidjeaneloge-ship-it/TP_Groupe_GitHub_Deploiement_Django
- **Application en ligne :** _à compléter après déploiement_
- **Groupe :** 5 — Sujet : Gestion de stock — Responsable : DJEAN BI ELOGE

## Fonctionnalités

- Liste des produits avec quantité, seuil d'alerte et badge de disponibilité.
- Filtre de la liste par catégorie (`/stock/?categorie=<id>`).
- Création d'un produit avec validation serveur (nom obligatoire, quantités entières positives,
  catégorie existante).
- Modification d'un produit avec formulaire pré-rempli.
- Suppression protégée : uniquement en `POST` + jeton CSRF, avec confirmation côté navigateur.
- Page « Alertes de stock » listant les produits sous leur seuil.
- Administration Django des catégories et des produits (recherche, filtres, édition en liste).
- Messages de succès/erreur après chaque action.

## Modèles

| Modèle | Champs | Relations |
|---|---|---|
| `Categorie` | `nom` (unique), `description` | possède plusieurs `Produit` (`related_name="produits"`) |
| `Produit` | `nom`, `quantite`, `seuil_alerte`, `date_ajout`, `date_modification` | `categorie` → `Categorie` (`ForeignKey`, `on_delete=CASCADE`) |

Deux modèles métier reliés par une `ForeignKey`, comme demandé dans le sujet.

## Structure du projet

```
config/                 # réglages, URLs racine, WSGI/ASGI
gestion/
  models.py             # Categorie, Produit
  views.py              # liste, création, modification, suppression, alertes, filtre
  urls.py               # namespace "opp_stock"
  admin.py              # enregistrement des deux modèles
  tests.py              # 24 tests (modèles, CRUD, validation, filtres, alertes)
  templates/opp_stock/  # base.html, produit_list.html, produit_form.html, alertes_stock.html
  migrations/           # 0001_initial
manage.py
requirements.txt
build.sh                # installation + collectstatic + migrate (hébergeur)
render.yaml             # configuration de déploiement Render
```

## URLs

| URL | Vue | Rôle |
|---|---|---|
| `/` | redirection | renvoie vers `/stock/` |
| `/stock/` | `liste_produits` | liste + filtre par catégorie |
| `/stock/produits/ajouter/` | `ajouter_produit` | formulaire de création |
| `/stock/produits/<pk>/modifier/` | `modifier_produit` | formulaire de modification |
| `/stock/produits/<pk>/supprimer/` | `supprimer_produit` | suppression (POST) |
| `/stock/categorie/<id>/` | `produits_par_categorie` | liste d'une catégorie |
| `/stock/alertes/` | `alertes_stock` | produits sous le seuil |
| `/admin/` | Django Admin | administration |

## Installation locale

Prérequis : Python 3.12+, pip et Git.

```bash
git clone https://github.com/goorebidjeaneloge-ship-it/TP_Groupe_GitHub_Deploiement_Django.git
cd TP_Groupe_GitHub_Deploiement_Django

python3 -m venv venv
source venv/bin/activate          # Windows : venv\Scripts\activate

pip install -r requirements.txt
python manage.py migrate
python manage.py donnees_demo     # facultatif : catégories et produits de démonstration
python manage.py runserver
```

Ouvrir ensuite http://127.0.0.1:8000/ (redirige vers `/stock/`).

Compte d'administration :

```bash
python manage.py createsuperuser
```

## Tests

```bash
python manage.py test
```

Couverture : `__str__` des modèles, règle d'alerte (strictement inférieure au seuil), suppression en
cascade, liste et filtre par catégorie, création valide et refusée (nom vide, quantité non numérique
ou négative, catégorie inexistante), modification, suppression (`GET` refusé en 405, `POST` accepté),
pages alertes et catégorie, redirection de la racine.

## Déploiement (Render, offre gratuite)

1. Sur [render.com](https://render.com) : **New → Web Service**, connecter le dépôt GitHub.
2. Render détecte `render.yaml` (sinon : build `./build.sh`, start
   `gunicorn config.wsgi:application`).
3. Variables d'environnement à définir :

   | Variable | Valeur |
   |---|---|
   | `SECRET_KEY` | valeur aléatoire générée par l'hébergeur |
   | `DEBUG` | `False` |
   | `ALLOWED_HOSTS` | `mondomaine.onrender.com` (ou `.onrender.com`) |
   | `CSRF_TRUSTED_ORIGINS` | `https://mondomaine.onrender.com` |
   | `PYTHON_VERSION` | `3.13.0` |

4. Le déploiement exécute automatiquement `collectstatic` puis `migrate` (voir `build.sh`).
5. Vérifier en ligne : la liste `/stock/`, un formulaire de création et la page `/stock/alertes/`.

> ⚠️ Sur l'offre gratuite, le disque est éphémère : la base SQLite peut être réinitialisée à chaque
> redémarrage. Pour une démonstration stable, relancer `python manage.py donnees_demo` via le Shell
> Render, ou brancher une base PostgreSQL managée (`DATABASE_URL`).

## Équipe et contributions

| Membre | Rôle | Branche | Pull Request |
|---|---|---|---|
| DJEAN BI ELOGE | Coordination, dépôt, intégration | `coordination` | _à compléter_ |
| ONIKOYAMOU Moïse | Modèles, ORM, migrations, Admin | `models` | _à compléter_ |
| KOUAKOU Christ Evrard | Vues, URLs, logique métier | `views` | _à compléter_ |
| KONE Mohamed Dia | Templates et formulaires | `templates` | _à compléter_ |
| KOUASSI Mihinsa Jean-Loïs | Tests, README, déploiement | `deploiement` | _à compléter_ |

Intégration : chaque branche personnelle est fusionnée dans `develop` (branche de test), puis
`develop` est fusionnée dans `main` via une Pull Request relue par un autre membre.

## Configuration de production

- `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS` et `CSRF_TRUSTED_ORIGINS` lus depuis l'environnement
  (aucun secret dans le dépôt).
- Fichiers statiques servis par **WhiteNoise** (`collectstatic` obligatoire au build).
- Cookies `Secure`, `X-Frame-Options: DENY` et `SECURE_CONTENT_TYPE_NOSNIFF` activés quand
  `DEBUG=False`.
- `gunicorn config.wsgi:application` comme serveur applicatif.
