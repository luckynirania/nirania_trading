# serializers.py
from rest_framework import serializers
from .models import Idea


class CustomIdeaSerializer(serializers.ModelSerializer):
    stock_name = serializers.CharField(source="stockName")
    suggested_price = serializers.FloatField(source="suggestedPrice")
    target_price = serializers.FloatField(source="targetPrice")
    closure_price = serializers.FloatField(source="nsePriceAtClosure")
    term = serializers.CharField()
    idea_creation_date = serializers.FloatField(source="createdAt")
    univest_status = serializers.CharField(source="status")
    univest_closure_reason = serializers.CharField(source="closureReason")
    exchange_status = serializers.CharField(
        source="ideastatus.status"
    )  # Assuming ideaStatus is the related name

    class Meta:
        model = Idea
        fields = [
            "stock_name",
            "suggested_price",
            "target_price",
            "closure_price",
            "term",
            "idea_creation_date",
            "univest_status",
            "univest_closure_reason",
            "exchange_status",
        ]


class LoopParamsSerializer(serializers.Serializer):
    times = serializers.IntegerField(min_value=1)
    delay = serializers.IntegerField(min_value=1)
