from django.urls import path

from . import views

app_name = "ads"

urlpatterns = [
    path("ads/invoice/<str:invoice_number>", views.ad_invoice, name="ad-invoice"),
    path("ad_click/<str:slug>", views.ad_clicks, name="ad_click"),
]
