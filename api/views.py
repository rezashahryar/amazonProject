import requests
from decimal import Decimal
from django.shortcuts import redirect, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProductSerializer, LinkSerializer
from bs4 import BeautifulSoup
from .models import Product, ProductProperty, SubLink, Size, ProductCategory, ProductColor
# Create your views here.

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0',
    'Referer': 'https://www.amazon.ae/',
    'Origin': 'https://www.amazon.ae',

}


@api_view(['POST'])
def get_product_info(request):
    if request.method == 'POST':
        serializer = LinkSerializer(data=request.data)
        if serializer.is_valid():
            link = serializer.data['link']

            res = requests.get(link, headers=header)

            # Split the URL by slash '/'
            url_parts = link.split('/')

            # Get the substring starting from the third slash to the end
            result = '/'.join(url_parts[:4])
            main_url = '{url}{slug}'
            content = BeautifulSoup(res.text, 'html.parser')

            title = content.find('span', attrs={'id': 'productTitle'}).text.strip()
            pricce = content.find('span', attrs={'class': 'a-offscreen'}).text.strip().replace("AED", "").replace(",", "")
            if pricce != "":
                if Decimal(90.00) < Decimal(pricce) < Decimal(100.00):
                    pricce = 100.00
            if pricce == "":
                # pricce = 123
                pricce = content.find('span', attrs={'class': 'a-price-whole'}).text.replace(",", "")
                # gheymat_v = content.find('span', attrs={'class': 'a-price-decimal'}).text
                # pricce = content.find('span', attrs={'class': 'a-price-fraction'}).text
                if Decimal(90.00) < Decimal(pricce) < Decimal(100.00):
                    pricce = 100.00

            size = None
            try:
                size = content.find('option', class_='dropdownSelect').text.strip()
            except:
                size = None

            images = None
            try:
                images = content.find_all('li', attrs={'class': "swatchAvailable"})
            except:
                images = None
            if images is not None:
                for image in images:
                    d = image.get('data-dp-url')
                    main_url = main_url.format(url=result, slug=d)
                    sub_link = SubLink.objects.create(link=main_url)
                    sub_link.save()

            product = Product.objects.create(title=title, price_AED=Decimal(pricce), size=size)
            product.save()
            properties = None
            try:
                properties = content.find('table', class_='a-spacing-micro')
            except:
                properties = None
            if properties is not None:
                rows = content.find_all('tr', class_='a-spacing-small')
                for row in rows:
                    title_of_property = row.find('td', class_='a-span3').text
                    value_of_property = row.find('td', class_='a-span9').text
                    product_properties = ProductProperty.objects.create(
                        product=product,
                        name=title_of_property,
                        value=value_of_property,
                    )
                    product_properties.save()

            second_type_properties = None
            try:
                second_type_properties = content.find_all('div', class_='product-facts-detail')
            except:
                second_type_properties = None

            if second_type_properties is not None:
                for property in second_type_properties:
                    title_of_property = property.find('div', class_='a-col-left').text.replace('\n', '').strip()
                    value_of_property = property.find('div', class_='a-col-right').text.replace('\n', '').strip()
                    product_properties = ProductProperty.objects.create(
                        product=product,
                        name=title_of_property,
                        value=value_of_property,
                    )
                    product_properties.save()

            sizes = None
            try:
                sizes = content.find_all('option', class_='dropdownAvailable')
            except:
                sizes = None

            if sizes is not None:
                for size in sizes:
                    product_size = Size.objects.create(
                        product=product,
                        size=size.text,
                    )
                    product_size.save()
                    product.available_size.add(product_size)

            categories = None
            try:
                categories = content.find_all('a', class_='a-color-tertiary')
            except:
                categories = None
            if categories is not None:
                for cat in categories:
                    product_cat = ProductCategory.objects.create(
                        product=product,
                        category=cat.text.strip()
                    )
                    product_cat.save()
                    product.category.add(product_cat)

            colors = None
            try:
                colors = content.find_all('img', class_='imgSwatch')
            except:
                colors = None

            if colors is not None:
                for c in colors:
                    print('&' * 90)
                    print(c.attrs.get('alt'))
                    product_color = ProductColor.objects.create(
                        product=product,
                        color=c.attrs.get('alt')
                    )
                    product_color.save()
                    product.colors.add(product_color)

            return redirect('api:show_product_info', product.pk)
        else:
            return Response(serializer.errors)


@api_view()
def show_product_info(request, pk):
    product = get_object_or_404(Product, pk=pk)
    serializer = ProductSerializer(product)
    return Response(serializer.data)