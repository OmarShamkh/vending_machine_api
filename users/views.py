from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly , IsAuthenticated
from .models import CustomUser 
from .serializers import UserSerializer
from django.http import Http404
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login, logout
from products.models import Product
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

class UserListCreate(APIView):

    @swagger_auto_schema(
        responses={200: "users list"},
        operation_description="Get all users"
    )
    def get(self, request):
        users = CustomUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password', 'role'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD, description='Password'),
                'role': openapi.Schema(type=openapi.TYPE_STRING, description='Role')
            },
        ),
        responses={201: "User created successfully"},
        operation_description="Create a new user"
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            raise Http404

    @swagger_auto_schema(
        responses={200: "User details"},
        operation_description="Get a user by ID",
        security=[{'Bearer': []}]
    )
    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD, description='Password'),
                'role': openapi.Schema(type=openapi.TYPE_STRING, description='Role')
            },
        ),
        responses={200: "User updated successfully"},
        operation_description="Update a user",
        security=[{'Bearer': []}]
    )
    def put(self, request, pk):
        user = self.get_object(pk)
        if request.user != user:
            return Response({'error': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={204: 'User was deleted successfully!'},
        operation_description="Delete a user",
        security=[{'Bearer': []}]
    )
    def delete(self, request, pk):
        user = self.get_object(pk)
        if request.user != user:
            return Response({'error': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)
        user.delete()
        message = {'message': 'User was deleted successfully!'}
        return Response(message ,  status=status.HTTP_204_NO_CONTENT)


# Authenticate users
class UserLogin(APIView):

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD),
            }
        ),
        responses={200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'access_token': openapi.Schema(type=openapi.TYPE_STRING)
            }
        )},
        operation_description="Log in a user"
    )
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return Response({
                'access_token': str(refresh.access_token),
            })
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class UserLogout(APIView):
    @swagger_auto_schema(
        responses={200: 'Successfully logged out'},
        operation_description="Logout a user",
        security=[{'Bearer': []}]
    )
    def post(self, request):
        logout(request)
        return Response({'message': 'Successfully logged out'})


# Deposit coins
class DepositView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'deposit': openapi.Schema(type=openapi.TYPE_INTEGER)
            }
        ),
        responses={200: "User details with updated deposit amount"},
        operation_description="Deposit coins",
        security=[{'Bearer': []}]
    )
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        deposit_amount = request.data.get('deposit')
        if deposit_amount is None:
            return Response({'error': 'Deposit amount is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if deposit_amount not in [5, 10, 20, 50, 100]:
            return Response({'error': 'Invalid deposit amount. Accepted values are 5, 10, 20, 50, and 100.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = request.user
        user.deposit += deposit_amount
        user.save()
        
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

# Buy products
class BuyView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'productId': openapi.Schema(type=openapi.TYPE_INTEGER),
                'amount': openapi.Schema(type=openapi.TYPE_INTEGER)
            }
        ),
        responses={200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'total_spent': openapi.Schema(type=openapi.TYPE_INTEGER),
                'products_purchased': openapi.Schema(type=openapi.TYPE_STRING),
                'change': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_OBJECT))
            }
        )},
        operation_description="Buy products",   
        security=[{'Bearer': []}]
    )
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        buyer = request.user
        if buyer.role != 'buyer':
            return Response({'error': 'Only users with a "buyer" role can buy products.'}, status=status.HTTP_403_FORBIDDEN)
        
        product_id = request.data.get('productId')
        amount = request.data.get('amount')
        if not product_id or not amount:
            return Response({'error': 'Both productId and amount are required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        
        if amount <= 0:
            return Response({'error': 'Invalid amount. Please provide a positive integer.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if amount > product.amountAvailable:
            return Response({'error': 'Insufficient stock.'}, status=status.HTTP_403_FORBIDDEN)
        
        total_cost = product.cost * amount
        if buyer.deposit < total_cost:
            return Response({'error': 'Insufficient funds.'}, status=status.HTTP_403_FORBIDDEN)
        
        buyer.deposit -= total_cost
        buyer.save()
        
        product.amountAvailable -= amount
        if product.amountAvailable <= 0:
            product.amountAvailable = 0
            
        product.save()
        
        change = buyer.deposit
        change_coins = []
        coins = [100, 50, 20, 10, 5]
        for coin in coins:
            num_coins = change // coin
            if num_coins > 0:
                change_coins.append({f'{coin} cent coins': num_coins})
                change -= num_coins * coin
        
        serializer = UserSerializer(buyer)
        response_data = {
            'total_spent': total_cost,
            'products_purchased': f'{amount} units of {product.productName}',
            'change': change_coins
        }
        return Response(response_data, status=status.HTTP_200_OK)


# Reset deposit
class ResetDeposit(APIView):
    @swagger_auto_schema(
        responses={200: "User details with reset deposit amount"},
        operation_description="Reset deposit",
        security=[{'Bearer': []}]
    )
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        buyer = request.user
        if buyer.role != 'buyer':
            return Response({'error': 'Only users with a "buyer" role can reset their deposit.'}, status=status.HTTP_403_FORBIDDEN)
        
        buyer.deposit = 0
        buyer.save()
        
        serializer = UserSerializer(buyer)
        return Response(serializer.data, status=status.HTTP_200_OK)