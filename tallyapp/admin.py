from django.contrib import admin

from tallyapp.models import groups,ledger,contra,account,Particulars,transactiontype,payment,bank,receipt,bankreceipt

# Register your models here.
admin.site.register(groups)
admin.site.register(ledger)
admin.site.register(contra)
admin.site.register(account)
admin.site.register(Particulars)
admin.site.register(transactiontype)
admin.site.register(payment)
admin.site.register(bank)
admin.site.register(receipt)
admin.site.register(bankreceipt)

