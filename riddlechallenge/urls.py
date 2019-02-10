"""riddlechallenge URL Configuration"""
from django.contrib import admin
from django.urls import path
from riddles.views import RiddleDetail

urlpatterns = [
    path("admin/", admin.site.urls),
    path("<uuid:pk>/", RiddleDetail.as_view(), name="riddle-detail"),
]
