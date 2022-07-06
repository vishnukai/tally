from django.urls import path

from tallyapp.models import receipt
from .import views
urlpatterns = [
    path('',views.home,name='home'),
    path('chequeprinting',views.chequeprinting,name='chequeprinting'),
    path('chequeregister',views.chequeregister,name='chequeregister'),
    path('searchbar',views.searchbar,name='searchbar'),
    path('searchledger',views.searchledger,name='searchledger'),
    path('chequep/<int:id>',views.chequep,name='chequep'),
    path('voucher/<int:id>',views.voucher,name='voucher'),
    path('updatepayment/<int:id>',views.updatepayment,name='updatepayment'),
    path('bankall/<int:id>',views.bankall,name='bankall'),
    path('savebank/<int:id>',views.savebank,name='savebank'),
    path('changecontra/<int:id>',views.changecontra,name='changecontra'),
    path('changepayment/<int:id>',views.changepayment,name='changepayment'),
    path('changerecipt/<int:id>',views.changerecipt,name='changerecipt'),
    path('updateconvertpayment/<int:id>',views.updateconvertpayment,name='updateconvertpayment'),
    path('updateconvertcontra/<int:id>',views.updateconvertcontra,name='updateconvertcontra'),
    path('updateconvertreceipt/<int:id>',views.updateconvertreceipt,name='updateconvertreceipt'),
    path('receiptbank/<int:id>',views.receiptbank,name='receiptbank'),
    path('savereceiptbank/<int:id>',views.savereceiptbank,name='savereceiptbank'),
    path('instrument/<int:id>',views.instrument,name='instrument'),
    path('montlysummary/<int:id>',views.monthlysummary,name='montlysummary'),
    path('getjune/<int:id>',views.getjune,name='getjune'),
    path('getjuly/<int:id>',views.getjuly,name='getjuly'),
    path('editreceipt/<int:id>',views.editreceipt,name='editreceipt'),
    path('getaugust/<int:id>',views.getaugust,name='getaugust'),
    path('getseptember/<int:id>',views.getseptember,name='getseptember'),
    path('getoctober/<int:id>',views.getoctober,name='getoctober'),
    path('getnovember/<int:id>',views.getnovember,name='getnovember'),
    path('getdecember/<int:id>',views.getdecember,name='getdecember'),
    path('getjanuary/<int:id>',views.getjanuary,name='getjanuary'),
    path('getfebruary/<int:id>',views.getfebruary,name='getfebruary'),
    path('getmarch/<int:id>',views.getmarch,name='getmarch'),
    path('getapril/<int:id>',views.getapril,name='getapril'),
    path('getmay/<int:id>',views.getmay,name='getmay'),


]