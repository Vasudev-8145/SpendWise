
from django.urls import path
from spending.views import SignUpView,GetMeView,ExpenseListCreateView,ExpenseRetrieveUpdateDeleteView

urlpatterns = [

    # authentication route
    path("register/",SignUpView.as_view()),

    # get me view rout
    path("me/",GetMeView.as_view()),

    # expense list create route
    path("expenses/",ExpenseListCreateView.as_view()),

    # expense retrive,update,delete route
    path("expenses/<int:pk>/",ExpenseRetrieveUpdateDeleteView.as_view()),
]