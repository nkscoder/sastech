from django.urls import path
from .views import *

category_list = CategoryViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

category_detail = CategoryViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

product_list = ProductViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

product_detail = ProductViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})



urlpatterns = [
    path('api/register/', RegisterUserView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/categories/', category_list, name='category-list'),
    path('api/categories/<int:pk>/', category_detail, name='category-detail'),
    path('api/products/', product_list, name='product-list'),
    path('api/products/<int:pk>/', product_detail, name='product-detail'),
    path('api/orders/', CreateOrderView.as_view(), name='create-order'),
]
