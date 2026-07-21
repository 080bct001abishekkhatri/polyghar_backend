from django.urls import path
from . import api

app_name = "shop"

urlpatterns = [
    path("api/health/", api.health, name="health"),
    path("api/products/", api.product_list, name="product_list"),
    path("api/products/<slug:slug>/", api.product_detail, name="product_detail"),
    path("api/settings/", api.settings_view, name="settings"),
]
