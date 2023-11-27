from .models import Product
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.reverse import reverse
from .review_serializers import ReviewSerializer
from .user_serializers import PublicUserSerializer


# This is the serializer for the products model
class ProductListSerializer(serializers.ModelSerializer):
    # Defining this attribute which will produce the url for the detail view
    detail_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'title',
            'price',
            'sale_item',
            'sale_price',
            'popular',
            'date_created',
            'detail_url'

        ]

    # Getting the url based on the user who is logged in
    def get_detail_url(self, obj):
        # Getting the request
        request = self.context.get('request')
        # Seeing if the user is a seller
        if request.user.groups.filter(name='seller').exists():
            return reverse("Seller:product-retrieve", kwargs={"pk": obj.pk}, request=request)
        else:
            return reverse("Buyer:product-retrieve", kwargs={"pk": obj.pk}, request=request)


# This serializer will handle serialization for the Detail View
class ProductDetailSerializer(serializers.ModelSerializer):
    popular = serializers.BooleanField(read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    seller = PublicUserSerializer(source="owner", read_only=True)
    date_created = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product

        fields = [
            'title',
            'price',
            'discount',
            'sale_price',
            'popular',
            'seller',
            'description',
            'date_created',
            'reviews'
        ]

    def get_date_created(self, obj):
        return obj.date_created.strftime("%Y-%m-%d")


# This serializer will handle the serialization for creating a new product
class ProductCreateSerializer(serializers.ModelSerializer):
    # Having a validator to ensure that each product name is unique
    title = serializers.CharField(max_length=200, validators=[UniqueValidator(queryset=Product.objects.all())])

    class Meta:
        model = Product

        fields = [
            'title',
            'price',
            'description',
            'discount',
        ]