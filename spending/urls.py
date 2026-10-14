
from django.urls import path
from spending.views import SignUpView,GetMeView,ExpenseListCreateView,ExpenseRetrieveUpdateDeleteView,ExpenseSummaryView,BudgetPlanView
from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns = [

    # authentication route
    path("register/",SignUpView.as_view()),

    # get me view rout
    path("me/",GetMeView.as_view()),

    # expense list create route
    path("expenses/",ExpenseListCreateView.as_view()),

    # expense retrive,update,delete route
    path("expenses/<int:pk>/",ExpenseRetrieveUpdateDeleteView.as_view()),

    # token creation route
    path("token/",ObtainAuthToken.as_view()),

    # expense summary route
    path("expenses/summary/",ExpenseSummaryView.as_view()),

    # budget plan view route
    path("expenses/budget/",BudgetPlanView.as_view()),

]