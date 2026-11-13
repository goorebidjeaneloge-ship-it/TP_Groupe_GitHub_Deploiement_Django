from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import F, Q
from django.views.decorators.http import require_POST, require_http_methods

from .models import Produit, Categorie


def categorie_id_depuis_get(request):
    """Retourne l'identifiant de catégorie demandé en GET, ou None s'il est absent ou invalide."""
    brut = request.GET.get("categorie", "")
    try:
        return int(brut)
    except (TypeError, ValueError):
        return None


@require_http_methods(["GET"])
def liste_produits(request):
    """Affiche les produits, avec filtre par catégorie et signalement des alertes."""
    categorie_id = categorie_id_depuis_get(request)

    produits = (
        Produit.objects
        .select_related("categorie")
        .annotate(en_alerte=Q(quantite__lt=F("seuil_alerte")))
        .order_by("nom")
    )
    if categorie_id is not None:
        produits = produits.filter(categorie_id=categorie_id)

    contexte = {
        "produits": produits,
        "categories": Categorie.objects.all().order_by("nom"),
        "categorie_selectionnee": categorie_id,
        "nombre_alertes": Produit.objects.filter(quantite__lt=F("seuil_alerte")).count(),
    }
    if categorie_id is not None:
        categorie = Categorie.objects.filter(pk=categorie_id).first()
        if categorie is not None:
            contexte["categorie_active"] = categorie

    return render(request, "opp_stock/produit_list.html", contexte)


def valider_donnees(request):
    """Valide les champs reçus depuis le formulaire produit."""
    nom = request.POST.get("nom", "").strip()
    quantite_brute = request.POST.get("quantite", "")
    seuil_brut = request.POST.get("seuil_alerte", "")
    categorie_id = request.POST.get("categorie", "")

    if not nom:
        return None, "Le nom du produit est obligatoire."

    try:
        quantite = int(quantite_brute)
        seuil_alerte = int(seuil_brut)
        if quantite < 0 or seuil_alerte < 0:
            return None, "Les quantités ne peuvent pas être négatives."
    except (ValueError, TypeError):
        return None, "La quantité et le seuil doivent être des nombres entiers."

    try:
        categorie = Categorie.objects.get(pk=categorie_id)
    except (Categorie.DoesNotExist, ValueError, TypeError):
        return None, "Veuillez sélectionner une catégorie valide."

    return {
        "nom": nom,
        "quantite": quantite,
        "seuil_alerte": seuil_alerte,
        "categorie": categorie,
    }, None


@require_http_methods(["GET", "POST"])
def ajouter_produit(request):
    """Affiche le formulaire et enregistre un nouveau produit."""
    categories = Categorie.objects.all().order_by("nom")

    if request.method == "POST":
        donnees, erreur = valider_donnees(request)
        if erreur:
            return render(request, "opp_stock/produit_form.html", {
                "categories": categories,
                "erreur": erreur,
                "donnees": request.POST,
            })

        Produit.objects.create(**donnees)
        messages.success(request, "Produit ajouté avec succès.")
        return redirect("opp_stock:liste_produits")

    return render(request, "opp_stock/produit_form.html", {
        "categories": categories,
    })


@require_http_methods(["GET", "POST"])
def modifier_produit(request, pk):
    """Modifie un produit existant."""
    produit = get_object_or_404(Produit, pk=pk)
    categories = Categorie.objects.all().order_by("nom")

    if request.method == "POST":
        donnees, erreur = valider_donnees(request)
        if erreur:
            return render(request, "opp_stock/produit_form.html", {
                "produit": produit,
                "categories": categories,
                "erreur": erreur,
                "donnees": request.POST,
            })

        for champ, valeur in donnees.items():
            setattr(produit, champ, valeur)
        produit.save()

        messages.success(request, "Produit modifié avec succès.")
        return redirect("opp_stock:liste_produits")

    return render(request, "opp_stock/produit_form.html", {
        "produit": produit,
        "categories": categories,
    })


@require_POST
def supprimer_produit(request, pk):
    """Supprime un produit uniquement via une requête POST."""
    produit = get_object_or_404(Produit, pk=pk)
    produit.delete()
    messages.success(request, "Produit supprimé avec succès.")
    return redirect("opp_stock:liste_produits")


@require_http_methods(["GET"])
def produits_par_categorie(request, categorie_id):
    """Affiche les produits appartenant à une catégorie donnée."""
    categorie = get_object_or_404(Categorie, pk=categorie_id)
    produits = (
        Produit.objects
        .filter(categorie=categorie)
        .select_related("categorie")
        .annotate(en_alerte=Q(quantite__lt=F("seuil_alerte")))
        .order_by("nom")
    )

    return render(request, "opp_stock/produit_list.html", {
        "produits": produits,
        "categories": Categorie.objects.all().order_by("nom"),
        "categorie_selectionnee": categorie_id,
        "categorie_active": categorie,
        "nombre_alertes": Produit.objects.filter(quantite__lt=F("seuil_alerte")).count(),
    })


@require_http_methods(["GET"])
def alertes_stock(request):
    """Affiche les produits dont la quantité est strictement sous le seuil."""
    produits = (
        Produit.objects
        .filter(quantite__lt=F("seuil_alerte"))
        .select_related("categorie")
        .order_by("quantite", "nom")
    )

    return render(request, "opp_stock/alertes_stock.html", {
        "produits": produits,
        "nombre_alertes": produits.count(),
    })