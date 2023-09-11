from django.urls import path

from angel_broking.views import (
    trigger_mapping_sheet_population,
    fetch_order_book_and_update_status,
)


urlpatterns = [
    path("fetch_symbol_data/", trigger_mapping_sheet_population),
    path("fetch_order_book_and_update_status", fetch_order_book_and_update_status),
]
