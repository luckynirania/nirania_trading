# admin.py
from django.contrib import admin
from .models import Idea, IdeaStatus, Order

admin.site.register(Idea)
admin.site.register(IdeaStatus)
admin.site.register(Order)
