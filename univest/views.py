# views.py
from django.http import JsonResponse
from rest_framework import viewsets, decorators, status
from .models import Idea
from .serializers import CustomIdeaSerializer, LoopParamsSerializer
from .tasks import loop_univest_fetch  # Import the function


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
        loop_univest_fetch(validated_data["times"], validated_data["delay"])
        return JsonResponse({"status": "loop triggered"})
    else:
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
