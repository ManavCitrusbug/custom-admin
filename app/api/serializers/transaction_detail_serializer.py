"""
This is a Serializer module.
Define your custom serializers here.
"""

from rest_framework import serializers
from customadmin.models import TransactionDetail

# -----------------------------------------------------------------------------
# TransactionDetail serializers
# -----------------------------------------------------------------------------


class TransactionDetailSerializer(serializers.ModelSerializer):
    """
    Serializes the TransactionDetail data into JSON
    """

    class Meta:
        """Define serializer properties in Meta class"""

        model = TransactionDetail
        fields = (
            "id",
            "user",
            "card_id",
            "customer_id",
            "charge_id",
            "charge_object",
            "amount",
            "amount_refunded",
            "application",
            "application_fee",
            "application_fee_amount",
            "balance_transaction",
            "address",
            "email",
            "name",
            "phone",
            "calculated_statement_descriptor",
            "captured",
            "created",
            "currency",
            "customer",
            "description",
            "disputed",
            "failure_code",
            "failure_message",
            "fraud_details",
            "invoice",
            "livemode",
            "metadata",
            "on_behalf_of",
            "order",
            "outcome",
            "paid",
            "payment_intent",
            "payment_method",
            "brand",
            "address_line1_check",
            "address_postal_code_check",
            "cvc_check",
            "country",
            "exp_month",
            "exp_year",
            "fingerprint",
            "funding",
            "installments",
            "last4",
            "network",
            "three_d_secure",
            "wallet",
            "charge_type",
            "receipt_email",
            "receipt_number",
            "receipt_url",
            "refunded",
            "refunds_object",
            "refunds_data",
            "refunds_has_more",
            "refunds_url",
            "review",
            "shipping",
            "source_transfer",
            "statement_descriptor",
            "statement_descriptor_suffix",
            "status",
            "transfer_data",
            "transfer_group",
            "source",
        )


class TransactionListingSerializer(serializers.ModelSerializer):
    """
    Transaction listing serializer
    """
    item_name = serializers.CharField()
    item_price = serializers.CharField()
    quantity = serializers.IntegerField()
    item_type = serializers.CharField()
    item_id = serializers.CharField()

    class Meta:
        model = TransactionDetail
        fields = ("id", "user", "transaction_id", "item_id", "item_name", "item_price", "quantity", "item_type", "created_at")
