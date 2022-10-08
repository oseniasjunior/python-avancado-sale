from django.urls import path
from core import consumers

urlrouter = [
    path('sale_channel/', consumers.SaleConsumer.as_asgi())
]
