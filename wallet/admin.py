from django.contrib import admin
from .models import Wallet, Transaction, PENDING, COMPLETED, DEPOSIT, WITHDRAW

admin.site.register(Wallet)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'wallet', 'amount', 'transaction_type', 'status', 'created_at')
    list_filter = ('transaction_type', 'status')
    actions = ['approve_transactions']

    @admin.action(description='Approve selected pending transactions')
    def approve_transactions(self, request, queryset):
        pending_transactions = queryset.filter(status=PENDING)
        for tx in pending_transactions:
            if tx.transaction_type == DEPOSIT:
                tx.wallet.balance += tx.amount
                tx.wallet.save(update_fields=['balance', 'updated_at'])
            elif tx.transaction_type == WITHDRAW:
                # Deduct from frozen_balance
                tx.wallet.frozen_balance -= tx.amount
                tx.wallet.save(update_fields=['frozen_balance', 'updated_at'])
            
            tx.status = COMPLETED
            tx.save(update_fields=['status', 'updated_at'])
        
        self.message_user(request, f"{pending_transactions.count()} transactions were approved.")
