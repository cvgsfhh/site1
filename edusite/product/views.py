from django.shortcuts import render

from product.models import Product, ProductContent, ContentCategory
from user.models import Users, Purchases


# Create your views here.
def product(request, slug):
    # my_products = Product.objects.get(slug=slug)
    my_products = ProductContent.objects.filter(product__slug=slug)
    my_product = my_products.first().product
    is_purchased = False
    if my_product.price !=0:
        if request.user.is_authenticated:
            user = Users.objects.get(user_email=request.user.email)
            purchased = Purchases.objects.filter(user=user,product=my_product)
            if purchased.exists():
                is_purchased = True
            else:
                is_purchased = False
    else:
        is_purchased = True
    content_category = ContentCategory.objects.filter(product=my_product)
    return render(request, template_name='product.html'
                  , context={'product': my_product, 'product_content': my_products,
                             'content_category': content_category,'is_purchased':is_purchased})
