from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework import status

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError


class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        print(f"Request data: {request.data}")
        return super().post(request, *args, **kwargs)

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username
        })

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer




class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        product_ids = request.data.get('products', [])
        products = []
        total_amount = 0
        out_of_stock_products = []

        for product_id in product_ids:
            try:
                product = Product.objects.get(id=product_id)
                if product.stock > 0:
                    products.append(product)
                    total_amount += product.price
                    product.stock -= 1  # Reduce stock
                    product.save()
                else:
                    out_of_stock_products.append(product.name)
            except Product.DoesNotExist:
                return Response({'error': f'Product with ID {product_id} does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        if out_of_stock_products:
            return Response({'error': f'Products {", ".join(out_of_stock_products)} are out of stock'}, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(user=request.user, total_amount=total_amount)
        order.products.set(products)
        order.save()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)