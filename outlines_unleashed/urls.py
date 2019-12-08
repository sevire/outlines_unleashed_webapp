from django.urls import path
from . import views


app_name = 'outlines_unleashed'  # here for namespacing of urls.

urlpatterns = [
    path("unleash-outline/", views.unleash_outline),
    path("result", views.result)
]