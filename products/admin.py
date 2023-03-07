from django.contrib import admin
from .models import ProductModel, PictureModel, ProductCategoryModel
from django.utils.html import mark_safe


class PictureInline(admin.StackedInline):
    def img_preview(self, obj):  # new
        return mark_safe(f'<img src = "{obj.picture.url}" width = "300"/>')

    extra = 0
    readonly_fields = ('img_preview',)
    model = PictureModel


@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):

    inlines = [PictureInline,]
    list_display = ('id', 'title')
    search_fields = ('id', 'title')


@admin.register(ProductCategoryModel)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('id', 'name')
