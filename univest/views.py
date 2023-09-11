# views.py
from django.http import JsonResponse
from rest_framework import viewsets, decorators, status
from univest.models import Idea
from univest.serializers import CustomIdeaSerializer, LoopParamsSerializer
from univest.tasks import loop_univest_fetch


class IdeaViewSet(viewsets.ModelViewSet):
    queryset = Idea.objects.select_related(
        "ideastatus"
    )  # Assuming the related name is ideaStatus
    serializer_class = CustomIdeaSerializer


@decorators.api_view(["GET"])
def trigger_loop(request):
    serializer = LoopParamsSerializer(data=request.GET)
    if serializer.is_valid():
        validated_data = serializer.validated_data
        try:
            loop_univest_fetch(validated_data["times"], validated_data["delay"])
            return JsonResponse({"message": "loop triggered"})
        except Exception as e:
            return JsonResponse(
                {"message": "loop not triggered: {}".format(e.message)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
    else:
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
