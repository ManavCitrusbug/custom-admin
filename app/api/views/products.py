from rest_framework.views import APIView
from customadmin.models import ShopProduct, PurchasedProduct, TransactionDetail
from ..serializers import ProductsListingSerializer, TransactionDetailSerializer
from numerology.permissions import get_pagination_response
from numerology.helpers import custom_response
from rest_framework import status
from numerology.utils import MyStripe, create_card_object, create_customer_id, create_charge_object
from numerology.permissions import IsAccountOwner


class ProductsListingAPIView(APIView):
    """
    Products listing View
    """
    serializer_class = ProductsListingSerializer

    def get(self, request):
        products = ShopProduct.objects.filter(active=True)
        result = get_pagination_response(products, request, self.serializer_class, context = {"request": request})
        message = "Products fetched Successfully!"
        return custom_response(True, status.HTTP_200_OK, message, result)



class PurchaseProductAPIView(APIView):
    """
    API View to purchase product
    """
    permission_classes = (IsAccountOwner,)

    def post(self, request, format=None):
        """POST method to create the data"""
        try:
            if "product_list" not in request.data:
                message = "Products are required!"
                return custom_response(False, status.HTTP_400_BAD_REQUEST, message)

            if "card_id" in request.data:
                card_id = request.data["card_id"]
                stripe = MyStripe()
                customer_id = request.user.customer_id

                if not customer_id:
                    newcustomer = create_customer_id(request.user)
                    customer_id = newcustomer.id
                    print("<<<-----|| CUSTOMER CREATED ||----->>>")
                newcard = stripe.create_card(customer_id, request.data)
                data = create_card_object(newcard, request)
                card_id = newcard.id
                print("<<<-----|| CARD CREATED ||----->>>")

                newcharge = stripe.create_charge(request.data, card_id, customer_id)
                charge_object = create_charge_object(newcharge, request)

                chargeserializer = TransactionDetailSerializer(data=charge_object)
                if chargeserializer.is_valid():
                    chargeserializer.save()
                    print("<<<-----|| TransactionDetail CREATED ||----->>>")

                    transaction = TransactionDetail.objects.filter(pk=chargeserializer.data['id'])
                    for product_item in request.data['product_list']:
                        product_obj = ShopProduct.objects.filter(pk=product_item['product'])
                        if not product_obj:
                            message = "Products not found!"
                            return custom_response(False, status.HTTP_400_BAD_REQUEST, message, result)

                        purchased_product = PurchasedProduct()
                        purchased_product.user = request.user
                        purchased_product.quantity = product_item['quantity']
                        purchased_product.product = product_obj[0]
                        purchased_product.product_price = product_obj[0].price
                        purchased_product.total_amount = product_obj[0].price * float(product_item['quantity'])
                        purchased_product.transaction_detail = transaction[0]
                        purchased_product.save()
                        message = "Products purchased successfully!"
                    return custom_response(True, status.HTTP_201_CREATED, message)
            else:
                message = "Card_id is required"
                return custom_response(False, status.HTTP_400_BAD_REQUEST, message)

        except Exception as inst:
            print(inst)
            message = str(inst)
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)