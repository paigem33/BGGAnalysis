from django.urls import path

from GBGAnalysisApp import views


urlpatterns = [
    path("reviews", views.reviews, name="reviews")
]