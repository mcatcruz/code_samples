from django.urls import path
from . import ecomeals_views

urlpatterns = [
    path("", views.index, name="index"),
    path('eco-meals', ecomeals_views.EcoMealsView.as_view()),
    path('eco-meals/<int:pk>', ecomeals_views.SingleUserAllEcoMealInstancesView.as_view()),
]