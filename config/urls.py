from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('stock/', include('gestion.urls')),
    # La racine redirige vers l'application de gestion de stock.
    path('', RedirectView.as_view(pattern_name='opp_stock:liste_produits', permanent=False)),
]
