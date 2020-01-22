from django.shortcuts import redirect
from django.urls import path
from . import views


app_name = 'ou_app'  # here for namespacing of urls.

urlpatterns = [
    path("unleash-outline/", views.unleash_outline),
    path("download-ppt/", views.download_ppt)
    # path("result", views.result)
]