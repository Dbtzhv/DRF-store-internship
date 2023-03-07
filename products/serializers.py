from rest_framework import serializers
from .models import ProductModel, PictureModel


class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = PictureModel
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    images = PictureSerializer(many=True, read_only=True)
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = ProductModel
        fields = ['id', 'title', 'category', 'description',
                  'price', 'general_quantity', 'images']
