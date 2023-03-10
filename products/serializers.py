from rest_framework import serializers
from .models import ProductModel, PictureModel, ProductCategoryModel, ParameterModel
from drf_extra_fields.fields import Base64ImageField
from drf_writable_nested import WritableNestedModelSerializer


class ParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParameterModel
        exclude = ('product',)


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategoryModel
        fields = '__all__'


class PictureSerializer(serializers.ModelSerializer):
    picture = Base64ImageField()

    class Meta:
        model = PictureModel
        exclude = ('product',)


class ProductSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    images = PictureSerializer(many=True, required=True)
    parameters = ParameterSerializer(many=True)
    # category = serializers.SlugRelatedField(slug_field='name', queryset=ProductCategoryModel.objects.all())

    class Meta:
        model = ProductModel
        fields = ['id', 'title', 'category', 'description',
                  'price', 'general_quantity', 'parameters', 'images']

    # def create(self, validated_data):
    #     choice_validated_data = validated_data.pop('images')
    #     product = ProductModel.objects.create(**validated_data)
    #     for i in choice_validated_data:
    #         PictureModel.objects.create(product=product, **i)
    #     return product
