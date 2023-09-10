from django.db import models
from django.forms import ValidationError
from django.utils import timezone
from django.db.models import JSONField
from auditlog.registry import auditlog
from .constants import (
    ORDER_STATUS_CHOICES,
    ORDER_TYPE_CHOICES,
    ORDER_SUB_TYPE_CHOICES,
    IdeaStatusChoices,
    OrderTypeChoices,
    OrderStatusChoices,
    IDEA_STATUS_CHOICES,
)


# Create Idea model
class Idea(models.Model):
    univest_id = models.IntegerField(unique=True)
    streamChannelId = models.CharField(max_length=255, null=True, blank=True)
    streamMessageId = models.CharField(max_length=255, null=True, blank=True)
    senderId = models.IntegerField()
    stockName = models.CharField(max_length=255)
    suggestedPrice = models.FloatField()
    expiresAt = models.BigIntegerField()
    targetPrice = models.FloatField()
    stopLoss = models.FloatField(null=True, blank=True)
    recommendationType = models.CharField(max_length=50)
    confidenceLevel = models.CharField(max_length=50, null=True, blank=True)
    closureReason = models.CharField(max_length=255, null=True, blank=True)
    bsePriceAtClosure = models.FloatField(null=True, blank=True)
    nsePriceAtClosure = models.FloatField(null=True, blank=True)
    createdAt = models.BigIntegerField()
    lastModified = models.BigIntegerField()
    channelName = models.CharField(max_length=255, null=True, blank=True)
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255, null=True, blank=True)
    senderContactNumber = models.CharField(max_length=20)
    profilePictureUrl = models.URLField(null=True, blank=True)
    open = models.BooleanField()
    hit = models.BooleanField()
    finCode = models.IntegerField()
    expectedDurationEnum = models.CharField(null=True, max_length=50)
    status = models.CharField(max_length=50)
    type = models.CharField(max_length=50, null=True, blank=True)
    watchListIds = JSONField(null=True, blank=True)
    analysis = models.TextField(null=True, blank=True)
    attachments = JSONField(null=True, blank=True)
    term = models.CharField(max_length=50)
    newTradeCard = models.BooleanField()
    locked = models.BooleanField()
    logoUrl = models.URLField(null=True, blank=True)
    compName = models.CharField(max_length=255, null=True, blank=True)
    netGain = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.stockName


class IdeaStatus(models.Model):
    idea = models.OneToOneField(Idea, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=50,
        choices=IDEA_STATUS_CHOICES,
        default="NEW",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.idea.stockName} - {self.status}"


class Order(models.Model):
    idea_status = models.ForeignKey(
        IdeaStatus,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Idea Status ID",
    )

    exchange_order_id = models.CharField(
        max_length=255, verbose_name="Exchange Order ID"
    )
    order_type = models.CharField(
        max_length=20, choices=ORDER_TYPE_CHOICES, verbose_name="Order Type"
    )
    order_sub_type = models.CharField(
        max_length=20, choices=ORDER_SUB_TYPE_CHOICES, verbose_name="Order Sub Type"
    )
    status = models.CharField(
        max_length=20, choices=ORDER_STATUS_CHOICES, verbose_name="Status"
    )
    price = models.FloatField(verbose_name="Price")
    quantity = models.IntegerField(verbose_name="Quantity")
    amount = models.FloatField(null=True, verbose_name="Amount")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    def __str__(self):
        return f"Order ID: {self.id}, Type: {self.order_type}, Status: {self.status}"

    def save(self, *args, **kwargs):
        self.amount = self.price * self.quantity

        if self.status not in [choice.name for choice in OrderStatusChoices]:
            raise ValidationError("Invalid order status.")

        if not self.pk:  # This is a new object
            if self.status != OrderStatusChoices.PLACED.name:
                raise ValidationError(
                    f"New orders can only be created with status '{OrderStatusChoices.PLACED.value}'."
                )

            status_mapping = {
                OrderTypeChoices.BUY.name: IdeaStatusChoices.BUY_ORDER_PLACED.name,
                OrderTypeChoices.SELL.name: IdeaStatusChoices.SELL_ORDER_PLACED.name,
            }

            new_status = status_mapping.get(self.order_type)
            if not new_status:
                raise ValidationError("Invalid order type.")

            if self.idea_status.status not in [
                IdeaStatusChoices.NEW.name,
                IdeaStatusChoices.BOUGHT.name,
            ]:
                raise ValidationError(
                    f"IdeaStatus must be either '{IdeaStatusChoices.NEW.value}' or '{IdeaStatusChoices.BOUGHT.value}'."
                )

            self.idea_status.status = new_status
            self.idea_status.save()

        else:  # This is an existing object
            if self.status == OrderStatusChoices.CANCELLED.name:
                if OrderStatusChoices.PLACED.name not in self.idea_status.status:
                    raise ValidationError(
                        f"Only {OrderStatusChoices.PLACED.value} orders can be cancelled."
                    )

                self.idea_status.status = self.idea_status.status.replace(
                    OrderStatusChoices.PLACED.name, OrderStatusChoices.CANCELLED.name
                )
                self.idea_status.save()

            elif self.status == OrderStatusChoices.EXECUTED.name:
                if OrderStatusChoices.PLACED.name not in self.idea_status.status:
                    raise ValidationError(
                        f"Only {OrderStatusChoices.PLACED.value} orders can be executed."
                    )

                if OrderTypeChoices.BUY.name in self.idea_status.status:
                    self.idea_status.status = IdeaStatusChoices.BOUGHT.name
                else:
                    self.idea_status.status = IdeaStatusChoices.SOLD.name

                self.idea_status.save()

        super(Order, self).save(*args, **kwargs)


auditlog.register(Idea)
auditlog.register(Order)
auditlog.register(IdeaStatus)
