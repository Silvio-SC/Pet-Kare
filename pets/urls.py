from django.urls import path
from .views import PetView, PetDateilView

urlpatterns = [
    path("pets/", PetView.as_view()),
    path("pets/<int:pet_id>/", PetDateilView.as_view()),
]
