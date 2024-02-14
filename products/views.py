# products/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Product
from .serializers import ProductSerializer
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
class ProductList(APIView):
    @swagger_auto_schema(
        responses={200: "products list"},
        operation_description="Get all products"
    )
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['productName', 'amountAvailable', 'cost'],
            properties={
                'productName': openapi.Schema(type=openapi.TYPE_STRING, description='Product name'),
                'amountAvailable': openapi.Schema(type=openapi.TYPE_INTEGER, description='Amount available'),
                'cost': openapi.Schema(type=openapi.TYPE_INTEGER, description='Cost'),
            },
        ),
        responses={201: "Product created successfully"},
        operation_description="Create a new product",
        security= [{'Bearer': []}]
    )
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

        serllerId = request.user.id
        request.data['sellerId'] = serllerId
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDetail(APIView):

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    @swagger_auto_schema(
        responses={200: "Product details"},
        operation_description="Get a product by ID"
    )
    def get(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'productName': openapi.Schema(type=openapi.TYPE_STRING, description='Product name'),
                'amountAvailable': openapi.Schema(type=openapi.TYPE_INTEGER, description='Amount available'),
                'cost': openapi.Schema(type=openapi.TYPE_INTEGER, description='Cost'),
            },
        ),
        responses={200: "Product updated successfully"},
        operation_description="Update a product",
        security= [{'Bearer': []}]
    )
    def put(self, request, pk):
        product = self.get_object(pk)
        sellerId = product.sellerId

        if not request.user.is_authenticated or request.user.id != sellerId.id:
            return Response({'error': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)
        
        request.data['sellerId'] = sellerId.id
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={204: 'Product deleted successfully!'},
        operation_description="Delete a product",
        security= [{'Bearer': []}]
    )
    def delete(self, request, pk):
        
        sellerId = Product.objects.get(pk=pk).sellerId
        if not request.user.is_authenticated or request.user.id != sellerId.id:
            return Response({'error': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)
        
        product = self.get_object(pk)
        product.delete()
        message = {'message': 'Product deleted successfully!'}
        return Response( message , status=status.HTTP_204_NO_CONTENT)
