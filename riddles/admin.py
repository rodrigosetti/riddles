from django.contrib import admin
from .models import Riddle

class RiddleAdmin(admin.ModelAdmin):
    list_display = ("title", "answer", "next")

admin.site.register(Riddle, RiddleAdmin)
