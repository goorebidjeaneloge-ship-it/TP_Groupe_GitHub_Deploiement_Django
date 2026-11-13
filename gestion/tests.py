from django.test import TestCase
from django.urls import reverse

from .models import Categorie, Produit


class ModeleProduitTests(TestCase):
    """Règles métier portées par les modèles."""

    def setUp(self):
        self.categorie = Categorie.objects.create(nom="Céréales")

    def test_str_categorie_et_produit(self):
        produit = Produit.objects.create(
            nom="Riz", categorie=self.categorie, quantite=10, seuil_alerte=5
        )
        self.assertEqual(str(self.categorie), "Céréales")
        self.assertEqual(str(produit), "Riz (10 en stock)")

    def test_produit_en_alerte_sous_le_seuil(self):
        produit = Produit.objects.create(
            nom="Riz", categorie=self.categorie, quantite=2, seuil_alerte=5
        )
        self.assertTrue(produit.est_en_alerte)

    def test_pas_d_alerte_a_quantite_egale_au_seuil(self):
        produit = Produit.objects.create(
            nom="Riz", categorie=self.categorie, quantite=5, seuil_alerte=5
        )
        self.assertFalse(produit.est_en_alerte)

    def test_suppression_categorie_supprime_ses_produits(self):
        Produit.objects.create(
            nom="Riz", categorie=self.categorie, quantite=10, seuil_alerte=5
        )
        self.categorie.delete()
        self.assertEqual(Produit.objects.count(), 0)


class ListeProduitsTests(TestCase):
    url = reverse("opp_stock:liste_produits")

    def setUp(self):
        self.cereales = Categorie.objects.create(nom="Céréales")
        self.boissons = Categorie.objects.create(nom="Boissons")
        self.riz = Produit.objects.create(
            nom="Riz", categorie=self.cereales, quantite=10, seuil_alerte=5
        )
        self.jus = Produit.objects.create(
            nom="Jus", categorie=self.boissons, quantite=1, seuil_alerte=5
        )

    def test_liste_affiche_tous_les_produits(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Riz")
        self.assertContains(response, "Jus")

    def test_filtre_par_categorie(self):
        response = self.client.get(self.url, {"categorie": self.boissons.pk})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Jus")
        self.assertNotContains(response, "Riz")

    def test_filtre_avec_categorie_invalide_ignore(self):
        response = self.client.get(self.url, {"categorie": "abc"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Riz")

    def test_badge_alerte_visible(self):
        response = self.client.get(self.url)
        self.assertContains(response, "Stock bas")
        self.assertContains(response, "Disponible")

    def test_racine_redirige_vers_la_liste(self):
        response = self.client.get("/")
        self.assertRedirects(response, self.url, fetch_redirect_response=False)


class CreationProduitTests(TestCase):
    url = reverse("opp_stock:ajouter_produit")

    def setUp(self):
        self.categorie = Categorie.objects.create(nom="Céréales")

    def test_formulaire_accessible(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nouveau produit")

    def test_creation_valide(self):
        response = self.client.post(self.url, {
            "nom": "Riz parfumé",
            "categorie": self.categorie.pk,
            "quantite": "12",
            "seuil_alerte": "5",
        })
        self.assertRedirects(response, reverse("opp_stock:liste_produits"))
        produit = Produit.objects.get(nom="Riz parfumé")
        self.assertEqual(produit.quantite, 12)
        self.assertEqual(produit.categorie, self.categorie)

    def test_creation_refusee_si_nom_vide(self):
        response = self.client.post(self.url, {
            "nom": "   ",
            "categorie": self.categorie.pk,
            "quantite": "12",
            "seuil_alerte": "5",
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Le nom du produit est obligatoire")
        self.assertEqual(Produit.objects.count(), 0)

    def test_creation_refusee_si_quantite_non_numerique(self):
        response = self.client.post(self.url, {
            "nom": "Riz",
            "categorie": self.categorie.pk,
            "quantite": "douze",
            "seuil_alerte": "5",
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "nombres entiers")
        self.assertEqual(Produit.objects.count(), 0)

    def test_creation_refusee_si_quantite_negative(self):
        response = self.client.post(self.url, {
            "nom": "Riz",
            "categorie": self.categorie.pk,
            "quantite": "-1",
            "seuil_alerte": "5",
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ne peuvent pas être négatives")
        self.assertEqual(Produit.objects.count(), 0)

    def test_creation_refusee_si_categorie_inconnue(self):
        response = self.client.post(self.url, {
            "nom": "Riz",
            "categorie": "999999",
            "quantite": "1",
            "seuil_alerte": "5",
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "catégorie valide")
        self.assertEqual(Produit.objects.count(), 0)


class ModificationProduitTests(TestCase):
    def setUp(self):
        self.categorie = Categorie.objects.create(nom="Céréales")
        self.produit = Produit.objects.create(
            nom="Riz", categorie=self.categorie, quantite=10, seuil_alerte=5
        )
        self.url = reverse("opp_stock:modifier_produit", args=[self.produit.pk])

    def test_formulaire_pre_rempli(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'value="Riz"')
        self.assertContains(response, 'value="10"')

    def test_modification_enregistree(self):
        response = self.client.post(self.url, {
            "nom": "Riz complet",
            "categorie": self.categorie.pk,
            "quantite": "42",
            "seuil_alerte": "8",
        })
        self.assertRedirects(response, reverse("opp_stock:liste_produits"))
        self.produit.refresh_from_db()
        self.assertEqual(self.produit.nom, "Riz complet")
        self.assertEqual(self.produit.quantite, 42)
        self.assertEqual(self.produit.seuil_alerte, 8)

    def test_modification_produit_inexistant_404(self):
        response = self.client.get(reverse("opp_stock:modifier_produit", args=[9999]))
        self.assertEqual(response.status_code, 404)


class SuppressionProduitTests(TestCase):
    def setUp(self):
        self.categorie = Categorie.objects.create(nom="Céréales")
        self.produit = Produit.objects.create(
            nom="Riz", categorie=self.categorie, quantite=10, seuil_alerte=5
        )
        self.url = reverse("opp_stock:supprimer_produit", args=[self.produit.pk])

    def test_get_interdit(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)
        self.assertTrue(Produit.objects.filter(pk=self.produit.pk).exists())

    def test_post_supprime_le_produit(self):
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse("opp_stock:liste_produits"))
        self.assertFalse(Produit.objects.filter(pk=self.produit.pk).exists())


class AlertesEtCategorieTests(TestCase):
    def setUp(self):
        self.cereales = Categorie.objects.create(nom="Céréales")
        self.boissons = Categorie.objects.create(nom="Boissons")
        self.riz = Produit.objects.create(
            nom="Riz", categorie=self.cereales, quantite=2, seuil_alerte=5
        )
        self.jus = Produit.objects.create(
            nom="Jus", categorie=self.boissons, quantite=50, seuil_alerte=5
        )

    def test_page_alertes_ne_montre_que_les_produits_sous_seuil(self):
        response = self.client.get(reverse("opp_stock:alertes_stock"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Riz")
        self.assertNotContains(response, "Jus")

    def test_page_categorie(self):
        response = self.client.get(
            reverse("opp_stock:produits_par_categorie", args=[self.cereales.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Riz")
        self.assertNotContains(response, "Jus")

    def test_categorie_inexistante_404(self):
        response = self.client.get(
            reverse("opp_stock:produits_par_categorie", args=[9999])
        )
        self.assertEqual(response.status_code, 404)


class AdminTests(TestCase):
    def test_admin_accessible(self):
        response = self.client.get("/admin/")
        self.assertEqual(response.status_code, 302)
