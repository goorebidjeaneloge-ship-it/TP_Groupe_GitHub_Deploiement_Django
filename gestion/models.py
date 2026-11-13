from django.db import models
from django.core.exceptions import ValidationError

class Categorie(models.Model):
    nom = models.CharField(max_length=100, unique=True, verbose_name="Nom de la catégorie")
    description = models.TextField(blank=True, null=True, verbose_name="Description")

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ['nom']

    def __str__(self):
        return self.nom


class Produit(models.Model):
    nom = models.CharField(max_length=150, verbose_name="Nom du produit")
    quantite = models.PositiveIntegerField(default=0, verbose_name="Quantité en stock")
    seuil_alerte = models.PositiveIntegerField(default=5, verbose_name="Seuil d'alerte")
    categorie = models.ForeignKey(
        Categorie,
        on_delete=models.CASCADE,
        related_name='produits',
        verbose_name="Catégorie"
    )
    date_ajout = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"
        ordering = ['nom']

    def __str__(self):
        return f"{self.nom} ({self.quantite} en stock)"

    @property
    def est_en_alerte(self):
        """Vrai si le stock est strictement inférieur au seuil d'alerte."""
        return self.quantite < self.seuil_alerte

    def clean(self):
        if self.nom and len(self.nom.strip()) < 2:
            raise ValidationError({'nom': "Le nom du produit doit contenir au moins 2 caractères."})