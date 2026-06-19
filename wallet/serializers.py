from rest_framework import serializers
from .models import Wallet, Transaction, DEPOSIT, WITHDRAW, PENDING

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['id', 'balance', 'frozen_balance', 'updated_at']
        read_only_fields = fields

class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['amount', 'card_number', 'receipt_image']

    def create(self, validated_data):
        wallet = self.context['request'].user.wallet
        return Transaction.objects.create(
            wallet=wallet,
            transaction_type=DEPOSIT,
            status=PENDING,
            **validated_data
        )

class WithdrawSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['amount', 'card_number']

    def validate(self, attrs):
        wallet = self.context['request'].user.wallet
        amount = attrs.get('amount')
        if wallet.balance < amount:
            raise serializers.ValidationError("Hisobingizda mablag' yetarli emas.")
        return attrs

    def create(self, validated_data):
        wallet = self.context['request'].user.wallet
        amount = validated_data['amount']
        
        # Deduct from balance and move to frozen_balance until admin approves
        wallet.balance -= amount
        wallet.frozen_balance += amount
        wallet.save(update_fields=['balance', 'frozen_balance', 'updated_at'])

        return Transaction.objects.create(
            wallet=wallet,
            transaction_type=WITHDRAW,
            status=PENDING,
            **validated_data
        )

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = fields
