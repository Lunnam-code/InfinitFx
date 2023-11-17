from django.contrib import admin
from . models import Inbox, Deposit, Investment, Plan


class InboxAdmin(admin.ModelAdmin):
  list_display = ('id', 'name', 'subject', 'sent_at')
  list_display_links = ('id','name', 'subject')
  readonly_fields = ('id', 'name','email','message', 'subject', 'sent_at')
  ordering = ('-sent_at',)


class DepositAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'amount', 'status')
    
    def save_model(self, request, obj, form, change):
        original_obj = Deposit.objects.get(pk=obj.pk) if change else None

        # Perform actions before saving the deposit object
        if obj.status == Deposit.APPROVED:
            obj.create_investment()
            
        elif change and original_obj.status == Deposit.APPROVED:
            # The deposit was previously approved and is now being changed to a different status
            # Reverse the previous action (e.g., delete the associated Investment object)
            try:
                investment = Investment.objects.get(deposit=original_obj)
                investment.delete()
            except Investment.DoesNotExist:
                pass  # Handle the case where the associated Investment object does not exist

        # Save the deposit object
        obj.save()

class InvestmentAdmin(admin.ModelAdmin):
  list_display = ('user', 'deposit', 'profit', 'created_at', 'status', 'maturity_duration_hour')

admin.site.register(Inbox, InboxAdmin)
admin.site.register(Deposit, DepositAdmin)
admin.site.register(Investment, InvestmentAdmin)
admin.site.register(Plan)