from django.urls import path
from . import views


app_name = 'ou_app'  # here for namespacing of urls.

urlpatterns = [
    path("unleash-outline/", views.unleash_outline),
    path("result", views.result)
]