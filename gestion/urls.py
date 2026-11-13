
from django.urls import path
from . import views

app_name = "opp_stock"

urlpatterns = [
    path("", views.liste_produits, name="liste_produits"),
    path("produits/ajouter/", views.ajouter_produit, name="ajouter_produit"),
    path("produits/<int:pk>/modifier/", views.modifier_produit, name="modifier_produit"),
    path("produits/<int:pk>/supprimer/", views.supprimer_produit, name="supprimer_produit"),
    path("categorie/<int:categorie_id>/", views.produits_par_categorie, name="produits_par_categorie"),
    path("alertes/", views.alertes_stock, name="alertes_stock"),
]
