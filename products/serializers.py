from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Product
from .validators import validate_title, unique_product_title
from api.serializers import UserPublicSerializer


class ProductSerializer(serializers.ModelSerializer):
    owner = UserPublicSerializer(source='user', read_only=True)
    url = serializers.HyperlinkedIdentityField(
        view_name="product-detail",
        lookup_field='pk'
    )
    edit_url = serializers.SerializerMethodField(read_only=True)
    # data validation in serializer
    title = serializers.CharField(validators=[unique_product_title])
    name = serializers.CharField(source='title', read_only=True)

    class Meta:
        model = Product
        fields = [
            'owner',
            'public',
            'url',
            'edit_url',
            'pk',
            'name',
            'title',
            'content',
            'price',
            'sale_price',
        ]

    def get_edit_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse("product-edit", kwargs={"pk": obj.pk}, request=request)

    # def validate_title(self, value):
    #     qs = Product.objects.filter(title__iexact=value)
    #     if qs.exists():
    #         raise serializers.ValidationError(
    #             f"{value} is already a product name.")
    #     return value
