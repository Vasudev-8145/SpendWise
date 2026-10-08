
from django.urls import path
from spending.views import SignUpView,GetMeView

urlpatterns = [

    # authentication route
    path("register/",SignUpView.as_view()),

    # get me view rout
    path("me/",GetMeView.as_view()),
]