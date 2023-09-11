from django.db import models


class SymbolTokenMappingSheet(models.Model):
    token = models.CharField(max_length=50)
    symbol = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    expiry = models.DateField(null=True, blank=True)
    strike = models.CharField(max_length=50)
    lotsize = models.IntegerField()
    instrumenttype = models.CharField(max_length=50, null=True, blank=True)
    exch_seg = models.CharField(max_length=20)
    tick_size = models.CharField(max_length=50)

    def __str__(self):
        return self.name
