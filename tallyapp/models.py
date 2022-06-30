

from django.db import models

# Create your models here.


class groups(models.Model):
    group=models.CharField(max_length=225)


    def __str__(self):
     return self.group

class ledger(models.Model):
    group=models.ForeignKey(groups,on_delete=models.CASCADE,blank=False)
    name=models.CharField(max_length=225)
    
    def __str__(self):
     return self.name

class transactiontype(models.Model):
    transactiontype=models.CharField(max_length=225)


class account(models.Model):
     
     account=models.ForeignKey(ledger,on_delete=models.CASCADE,blank=False)
     date=models.DateTimeField()

class Particulars(models.Model):
    particualrs=models.ForeignKey(ledger,on_delete=models.CASCADE,blank=False)
    amount=models.IntegerField()


class contra(models.Model):
    
    no=models.IntegerField()   
    date=models.ForeignKey(account,on_delete=models.CASCADE,blank=False)
    amount=models.ForeignKey(Particulars,on_delete=models.CASCADE,blank=False)

class payment(models.Model):
    
    no=models.IntegerField()   
    date=models.ForeignKey(account,on_delete=models.CASCADE,blank=False)
    amount=models.ForeignKey(Particulars,on_delete=models.CASCADE,blank=False)

class bank(models.Model):
    ledger=models.ForeignKey(ledger,on_delete=models.CASCADE,blank=False)
    transactiontype=models.ForeignKey(transactiontype,on_delete=models.CASCADE,blank=False)
    instno=models.IntegerField()
    instdate=models.DateField()
    amount=models.ForeignKey(Particulars,on_delete=models.CASCADE,blank=False)
    date=models.ForeignKey(account,on_delete=models.CASCADE,blank=False)
    
class receipt(models.Model):
    no=models.IntegerField()   
    date=models.ForeignKey(account,on_delete=models.CASCADE,blank=False)
    amount=models.ForeignKey(Particulars,on_delete=models.CASCADE,blank=False)

class bankreceipt(models.Model):
    ledger=models.ForeignKey(ledger,on_delete=models.CASCADE,blank=False)
    transactiontype=models.ForeignKey(transactiontype,on_delete=models.CASCADE,blank=False)
    instno=models.IntegerField()
    instdate=models.DateField()
    amount=models.ForeignKey(Particulars,on_delete=models.CASCADE,blank=False)
    date=models.ForeignKey(account,on_delete=models.CASCADE,blank=False)
     

   
 


