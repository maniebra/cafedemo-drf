from .views import *
from django.urls import path

urlpatterns = [
    path('reviews/', ReviewsNoParamView.as_view()),
    path('reviews/<int:id>/', ReviewsParamsView.as_view()),
    path('submit_review/<int:orderid>/', SubmitReviewView.as_view())
]
