from django.db import models
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
    expectedDurationEnum = models.CharField(null=True,max_length=50)
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

auditlog.register(Idea)