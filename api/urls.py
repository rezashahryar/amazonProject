from django.urls import path
from . import views
# create your urls here

app_name = 'api'

urlpatterns = [
   path('get-product-info/', views.get_product_info, name='get_product_info'),
   path('show-product-info/<int:pk>/', views.show_product_info, name='show_product_info'),
]