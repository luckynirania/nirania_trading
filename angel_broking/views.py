# views.py
from django.http import JsonResponse
from rest_framework import decorators, status

from angel_broking.tasks import (
    call_open_api_to_populate_mapping_sheet,
    get_trade_book_and_update_order_status,
)


@decorators.api_view(["GET"])
def trigger_mapping_sheet_population(request):
    try:
        call_open_api_to_populate_mapping_sheet()
        return JsonResponse({"message": "call triggered"})
    except Exception as e:
        return JsonResponse(
            {"message": "call not triggered: {}".format(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@decorators.api_view(["GET"])
def fetch_order_book_and_update_status(request):
    try:
        get_trade_book_and_update_order_status()
        return JsonResponse({"message": "call triggered"})
    except Exception as e:
        return JsonResponse(
            {"message": "call not triggered: {}".format(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
