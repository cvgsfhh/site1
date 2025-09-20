from django.contrib import admin

from product.models import Product, ContentCategory, ProductContent

# Register your models here.
admin.site.register(Product)
admin.site.register(ContentCategory)
admin.site.register(ProductContent)
