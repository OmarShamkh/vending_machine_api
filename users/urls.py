from django.urls import path
from .views import UserListCreate, UserDetail, UserLogin, UserLogout , DepositView , BuyView, ResetDeposit

urlpatterns = [
    path('', UserListCreate.as_view(), name='user-list'),
    path('<int:pk>/', UserDetail.as_view(), name='user-detail'),
    path('login/', UserLogin.as_view(), name='user-login'),
    path('logout/', UserLogout.as_view(), name='user-logout'),
    path('deposit/', DepositView.as_view(), name='user-deposit'),
    path('reset-deposit/', ResetDeposit.as_view(), name='user-reset-deposit'),
    path('buy/', BuyView.as_view(), name='user-withdraw'),
]
