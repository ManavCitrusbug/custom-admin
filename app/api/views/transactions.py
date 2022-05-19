from rest_framework.views import APIView
from customadmin.models import TransactionDetail, BookedService, PurchasedProduct
from ..serializers import TransactionListingSerializer
from numerology.permissions import get_pagination_response
from numerology.helpers import custom_response
from rest_framework import status
from numerology.permissions import IsAccountOwner


class TransactionListingAPIView(APIView):
    """
    Testimonials listing View
    """
    serializer_class = TransactionListingSerializer
    permission_classes = (IsAccountOwner,)

    def get(self, request):
        transactions = TransactionDetail.objects.filter(user=request.user.pk)
        month = request.GET.get('month', None)
        year = request.GET.get('year', None)

        if month:
            transactions = transactions.filter(created_at__date__month=month)

        if year:
            transactions = transactions.filter(created_at__date__year=year)

        transaction_list = []
        for transaction in transactions:
            is_service = BookedService.objects.filter(transaction_detail=transaction.pk)
            transaction.item_type = "service" if is_service else "product"
            
            if is_service:
                transaction.item_name = is_service[0].service.name
                transaction.item_price = is_service[0].booking_charge
                transaction.item_id = is_service[0].pk
                transaction.quantity = 1
                transaction_list.append(transaction)
            else:
                products = PurchasedProduct.objects.filter(transaction_detail=transaction.pk)
                if products:
                    for product in products:
                        transaction.item_name = product.product.name
                        transaction.item_price = product.product_price
                        transaction.quantity = product.quantity
                        transaction.item_id = product.pk
                        transaction_list.append(transaction)


        result = get_pagination_response(transaction_list, request, self.serializer_class, context = {"request": request})
        message = "Transactions fetched Successfully!"
        return custom_response(True, status.HTTP_200_OK, message, result)


class TransactionDetailAPIView(APIView):
    """
    Testimonials listing View
    """
    serializer_class = TransactionListingSerializer
    permission_classes = (IsAccountOwner,)

    def get(self, request, pk):
        transaction = TransactionDetail.objects.filter(pk=pk)

        transaction_list = []
        if transaction:
            is_service = BookedService.objects.filter(transaction_detail=pk)
            transaction[0].item_type = "service" if is_service else "product"
            
            if is_service:
                transaction[0].item_name = is_service[0].service.name
                transaction[0].item_price = is_service[0].booking_charge
                transaction[0].item_id = is_service[0].pk
                transaction[0].quantity = 1
                transaction_list.append(transaction[0])
            else:
                products = PurchasedProduct.objects.filter(transaction_detail=pk)
                if products:
                    for product in products:
                        transaction[0].item_name = product.product.name
                        transaction[0].item_price = product.product_price
                        transaction[0].quantity = product.quantity
                        transaction[0].item_id = product.pk
                        transaction_list.append(transaction[0])

            result = get_pagination_response(transaction_list, request, self.serializer_class, context = {"request": request})
            message = "Transaction detail fetched Successfully!"
            return custom_response(True, status.HTTP_200_OK, message, result)
        message = "Transaction not found!"
        return custom_response(True, status.HTTP_200_OK, message)