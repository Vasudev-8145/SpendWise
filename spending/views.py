
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Sum

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication,permissions

from datetime import datetime

from spending.serializers import UserSerializer,ExpenseSerializer
from spending.models import Expense
from spending.permissions import IsOwner

class SignUpView(APIView):

    def post(self,request):

        form_data = request.data

        serializer_instance = UserSerializer(data=form_data)

        if serializer_instance.is_valid():

            cleaned_data = serializer_instance.validated_data

            instance = User.objects.create_user(**cleaned_data)

            serializer_instance = UserSerializer(instance)

            return Response(data=serializer_instance.data)

        else:

            return Response(data=serializer_instance.errors)

class GetMeView(APIView):

    # authentication_classes = [authentication.BasicAuthentication]
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):

        auth_user = request.user

        instance = User.objects.get(username=auth_user)

        serializer_instance = UserSerializer(instance)

        return Response(data=serializer_instance.data)

class ExpenseListCreateView(APIView):

    # authentication_classes = [authentication.BasicAuthentication]
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):

        instance = Expense.objects.filter(owner=request.user)

        serializer_instance = ExpenseSerializer(instance,many=True)

        return Response(data=serializer_instance.data)

    def post(self,request):

        form_data = request.data

        serializer_instance = ExpenseSerializer(data=form_data)

        if serializer_instance.is_valid():

            serializer_instance.save(owner=request.user)

            return Response(data=serializer_instance.data)

        else:

            return Response(data=serializer_instance.errors)

class ExpenseRetrieveUpdateDeleteView(APIView):

    # authentication_classes = [authentication.BasicAuthentication]
    authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [IsOwner]

    def get(self,request,pk=None):

        instance = get_object_or_404(Expense,id=pk)

        self.check_object_permissions(request,instance)

        serializer_instance = ExpenseSerializer(instance)

        return Response(data=serializer_instance.data)

    def put(self,request,pk=None):

        instance = get_object_or_404(Expense,id=pk)

        self.check_object_permissions(request,instance)

        form_data = request.data

        serializer_instance = ExpenseSerializer(data=form_data,instance=instance)

        if serializer_instance.is_valid():

            serializer_instance.save()

            return Response(data=serializer_instance.data)

        else:

            return Response(data=serializer_instance.errors)

    def delete(self,request,pk=None):

        instance = get_object_or_404(Expense,id=pk)

        self.check_object_permissions(request,instance)

        instance.delete()

        return Response(data={"message":"deleted"})

class ExpenseSummaryView(APIView):

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):

        response_data = {
            "todays_total":0,
        }

        cur_date = datetime.now().date()
        cur_month = datetime.now().month
        cur_year = datetime.now().year

        # todays transaction summary

        todays_transactions = Expense.objects.filter(owner=request.user,created_at__date=cur_date)

        if todays_transactions:

            today_exp = todays_transactions.values("amount").aggregate(total=Sum("amount")).get("total")

            today_categ_sum = todays_transactions.values("category").annotate(total=Sum("amount"))

            response_data["todays_total"] = today_exp

            response_data["today_category_summary"] = today_categ_sum

        # monthly transaction summary

        monthly_transactions = Expense.objects.filter(owner=request.user,created_at__month=cur_month,created_at__year=cur_year)

        if monthly_transactions:

            month_exp = monthly_transactions.values("amount").aggregate(total=Sum("amount")).get("total")

            month_cat_summ = monthly_transactions.values("category").annotate(total=Sum("amount"))

            response_data["monthly_total"] = month_exp
            response_data["monthly_category_total"] = month_cat_summ

        return Response(data=response_data)

