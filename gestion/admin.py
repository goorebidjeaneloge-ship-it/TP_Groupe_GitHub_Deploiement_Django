from django.contrib import admin
from .models import Categorie, Produit

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('nom', 'description', 'nombre_produits')
    search_fields = ('nom',)

    def nombre_produits(self, obj):
        return obj.produits.count()
    nombre_produits.short_description = "Nombre de produits"


@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ('nom', 'categorie', 'quantite', 'seuil_alerte', 'alerte_stock')
    list_filter = ('categorie',)
    search_fields = ('nom',)
    list_editable = ('quantite', 'seuil_alerte')

    def alerte_stock(self, obj):
        return "STOCK BAS" if obj.est_en_alerte else "OK"
    alerte_stock.short_description = "État du stock"