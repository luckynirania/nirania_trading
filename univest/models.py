from django.db import models
from django.forms import ValidationError
from django.utils import timezone
from django.db.models import JSONField
from auditlog.registry import auditlog


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
        choices=[
            ("NEW", "New"),
            ("BUY_ORDER_PLACED", "Buy Order Placed"),
            ("BOUGHT", "Bought"),
            ("SELL_GTT_ORDER_PLACED", "Sell GTT Order Placed"),
            ("SOLD", "Sold and Closed"),
            ("EXPIRED", "Idea was already Closed"),
        ],
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

    TYPE_CHOICES = [
        ("SELL", "Sell"),
        ("BUY", "Buy"),
        ("GTT_SELL", "GTT Sell"),
        ("GTT_BUY", "GTT Buy"),
    ]

    STATUS_CHOICES = [
        ("PLACED", "Placed"),
        ("CANCELLED", "Cancelled"),
        ("EXECUTED", "Executed"),
    ]

    exchange_order_id = models.CharField(
        max_length=255, verbose_name="Exchange Order ID"
    )
    order_type = models.CharField(
        max_length=20, choices=TYPE_CHOICES, verbose_name="Order Type"
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, verbose_name="Status"
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
        if self.idea_status:
            # Constraint for order_type='BUY' and status='PLACED'
            if self.order_type == "BUY" and self.status == "PLACED":
                if self.idea_status.status != "NEW":
                    raise ValidationError(
                        "Only IdeaStatus with status 'NEW' can have an order of type 'BUY' and status 'PLACED'"
                    )
                else:
                    self.idea_status.status = "BUY_ORDER_PLACED"
                    self.idea_status.save()

            # Constraint for changing status from 'PLACED' to 'EXECUTED'
            elif self.status == "EXECUTED":
                if self.idea_status.status != "BUY_ORDER_PLACED":
                    raise ValidationError(
                        "Only IdeaStatus with status 'BUY_ORDER_PLACED' can change to an order status of 'EXECUTED'"
                    )
                else:
                    self.idea_status.status = "BOUGHT"
                    self.idea_status.save()

        super(Order, self).save(*args, **kwargs)


auditlog.register(Idea)
auditlog.register(Order)
auditlog.register(IdeaStatus)
