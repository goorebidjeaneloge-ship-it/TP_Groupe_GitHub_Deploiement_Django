"""Commande de démonstration : `python manage.py donnees_demo`."""

from django.core.management.base import BaseCommand
from django.db.models import F

from gestion.models import Categorie, Produit


CATEGORIES = [
    ("Céréales", "Riz, maïs, farine"),
    ("Boissons", "Jus, eau, sodas"),
    ("Hygiène", "Savon, détergent, papier"),
]

PRODUITS = [
    # (nom, catégorie, quantité, seuil d'alerte)
    ("Riz parfumé 5 kg", "Céréales", 42, 10),
    ("Maïs concassé 1 kg", "Céréales", 8, 10),
    ("Farine de blé 1 kg", "Céréales", 25, 5),
    ("Jus d'orange 1 L", "Boissons", 60, 15),
    ("Eau minérale 1,5 L", "Boissons", 12, 24),
    ("Savon de Marseille", "Hygiène", 3, 6),
]


class Command(BaseCommand):
    help = "Crée un jeu de données de démonstration (catégories et produits)."

    def handle(self, *args, **options):
        categories = {}
        for nom, description in CATEGORIES:
            categorie, creee = Categorie.objects.get_or_create(
                nom=nom, defaults={"description": description}
            )
            categories[nom] = categorie
            etat = "Créée" if creee else "Déjà présente"
            self.stdout.write(f"{etat} : catégorie {categorie.nom}")

        for nom, categorie_nom, quantite, seuil in PRODUITS:
            produit, cree = Produit.objects.get_or_create(
                nom=nom,
                categorie=categories[categorie_nom],
                defaults={"quantite": quantite, "seuil_alerte": seuil},
            )
            etat = "Créé" if cree else "Déjà présent"
            self.stdout.write(f"{etat} : produit {produit.nom}")

        total = Produit.objects.count()
        en_alerte = Produit.objects.filter(quantite__lt=F("seuil_alerte")).count()
        self.stdout.write(
            self.style.SUCCESS(
                f"Terminé : {total} produit(s), {en_alerte} en alerte de stock."
            )
        )
