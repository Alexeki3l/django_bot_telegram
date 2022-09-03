from bot.views import tbot
from django.urls import path

urlpatterns = [
    path('', tbot, name="tbot"),
]