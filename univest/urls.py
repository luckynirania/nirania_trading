from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import IdeaViewSet, trigger_loop

router = DefaultRouter()
router.register(r"ideas", IdeaViewSet)

urlpatterns = [
    path("trigger_loop/", trigger_loop),
]

urlpatterns += router.urls
