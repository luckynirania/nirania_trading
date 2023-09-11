# views.py
from django.http import JsonResponse
from rest_framework import decorators, status

from angel_broking.tasks import call_open_api_to_populate_mapping_sheet


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
