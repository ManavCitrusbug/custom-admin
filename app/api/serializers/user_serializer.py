from rest_framework import fields, serializers
from customadmin.models import User, ProductCart, ServiceCart
from rest_framework.authtoken.models import Token
from numerology.utils import MyStripe


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    User Profile serializer
    """
    email = serializers.EmailField()
    token = serializers.SerializerMethodField(read_only=True)
    password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(read_only=True, required=False)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'token', 'password', 'confirm_password', 'profile_image', 'date_of_birth', 'language', 'phone']
    
        extra_kwargs = {"password":
                                {"write_only": True}
                            }

    def create(self, validated_data):
        """
        custom 'create' so that password gets hashed!
        """
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()

        # Create Stripe customer ID
        stripe = MyStripe()
        customer = stripe.create_customer(instance)
        instance.customer_id = customer.id
        instance.save()
        return instance


    def get_token(self, obj):
        return f"Token {Token.objects.get_or_create(user=obj)[0]}"


class UserLoginSerializer(serializers.ModelSerializer):
    """
    User Profile serializer
    """
    cart_count = serializers.SerializerMethodField()
    cart_type = serializers.SerializerMethodField()
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'profile_image', 'token', 'date_of_birth', 'language', 'cart_count', 'cart_type']
    
    def get_cart_count(self, instance):
        products = ProductCart.objects.filter(user=instance.pk)
        if products:
            return products.count()
        services = ServiceCart.objects.filter(user=instance.pk)
        if services:
            return services.count()
        return 0

    def get_cart_type(self, instance):
        products = ProductCart.objects.filter(user=instance.pk)
        if products:
            return 'product_cart'
        services = ServiceCart.objects.filter(user=instance.pk)
        if services:
            return 'service_cart'
        return 'empty_cart'

    def get_token(self, obj):
        return f"Token {Token.objects.get_or_create(user=obj)[0]}"