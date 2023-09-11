from django.urls import path

from angel_broking.views import trigger_mapping_sheet_population


urlpatterns = [
    path("fetch_symbol_data/", trigger_mapping_sheet_population),
]
