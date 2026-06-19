from django.urls import path
from .views import WalletDetailAPIView, DepositAPIView, WithdrawAPIView, TransactionListAPIView

urlpatterns = [
    path('wallet/', WalletDetailAPIView.as_view(), name='wallet-detail'),
    path('wallet/deposit/', DepositAPIView.as_view(), name='wallet-deposit'),
    path('wallet/withdraw/', WithdrawAPIView.as_view(), name='wallet-withdraw'),
    path('wallet/transactions/', TransactionListAPIView.as_view(), name='wallet-transactions'),
]
