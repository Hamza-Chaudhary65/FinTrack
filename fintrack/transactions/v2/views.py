from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from transactions.models import Transaction
from transactions.serializer import TransactionSerializer
from transactions.transaction_helper import TransactionManager
from rest_framework.viewsets import ViewSet
transaction_manager = TransactionManager()


class TransactionAPIView(APIView):

    def get(self, request):
        transactions = Transaction.objects.filter(transaction_from_account__in=request.user.bank_accounts.all())

        paginator = PageNumberPagination()
        paginated_transactions = paginator.paginate_queryset(transactions, request)

        serializer = TransactionSerializer(paginated_transactions, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):

        serializer = TransactionSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        transaction_manager.handle_new_transaction(serializer.validated_data)
        return Response(serializer.data)   


class TransactionDetailAPIView(APIView):

    def get(self, request, pk):
        transaction = get_object_or_404(
            Transaction, 
            pk=pk, 
            transaction_from_account__holder=request.user
        )
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)


class RevertTransactionAPIView(APIView):

    def post(self, request, pk):
        transaction = get_object_or_404(
            Transaction, 
            pk=pk, 
            transaction_from_account__holder=request.user
        )

        if transaction.is_reverted:
            response = Response(
                { "message": "Can not revert this transaction"}, 
                status= status.HTTP_400_BAD_REQUEST
            )
        else:
            transaction_manager.handle_revert_transaction(transaction, request.data)
            response = Response(
                { "message": "Reverted Successfully"}
            )

        return response
