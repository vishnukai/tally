
import datetime
from django.shortcuts import render, redirect
from tallyapp.models import  Particulars, groups,ledger,bank,contra,payment,account, receipt, transactiontype,Vouchertype
from django.db.models import Count
from django.contrib import messages
import datetime
import fiscalyear
from fiscalyear import *
from dateutil import relativedelta
from django.db.models import Q



# Create your views here.
def home(request):
    return render(request,'base.html')

def chequeprinting(request):
    return render(request,'chequeprinting.html')

def chequeregister(request):
    # bab=bank.objects.values('ledger').Count('ledger')
    # print(bab)
    v=Vouchertype.objects.all()
    for v in v:
        if v.vouchertype=="Contra":
            vid=v.id
        elif v.vouchertype=="Payment":
            pid=v.id
        else:
            pass

    t=transactiontype.objects.all()
    for t in t:
        if t.transactiontype=="Cheque":
            tid=t.id
    todays_date = datetime.date.today()
    b=bank.objects.filter(Q(vouchertype=vid)|Q (vouchertype=pid)).filter(transactiontype=tid).values('ledger').annotate(total=Count('ledger'))
    c=bank.objects.filter(Q(vouchertype=vid)|Q (vouchertype=pid)).filter(transactiontype=tid).filter(instdate__lte=todays_date).values('ledger').annotate(total=Count('ledger'))
    print(c)
    print(b)
    bak=ledger.objects.all()
   
    # bak=list(b)
    # a_list = []     

    # for i in range(0,len(bak)):

    #     a=bak[i]
    #     for i in a:
    #         if i == "ledger":
                
    #             uid=a[i]
    #             led=ledger.objects.get(id=uid)
    #             c=led.name
    #             a.update({'ledger':c})
    #             a_list.append(a)
               
                
                
    #         else:
    #             pass
    
    # group=groups.objects.get(group="Bank Account")
    

    # led=ledger.objects.filter(group=group.id)  
    # new        
    return render(request,'chequeregister.html',{'l':b,'bak':bak,'c':c})




def searchbar(request):
    group=groups.objects.get(group="Bank Account")
    led=ledger.objects.filter(group=group.id)
    return render(request,'searchbar.html',{'l':led})

def searchledger(request):
    group=groups.objects.get(group="Bank Account")
    led=ledger.objects.filter(group=group.id)
    return render(request,'searhbarledger.html',{'l':led})


def chequep(request,id):
    sum=0
    led=ledger.objects.get(id=id)
    uid=led.id
    v=Vouchertype.objects.all()
    for v in v:
        if v.vouchertype=="Contra":
            vid=v.id
        elif v.vouchertype=="Payment":
            pid=v.id
        else:
            pass
    t=transactiontype.objects.all()
    for t in t:
        if t.transactiontype=="Cheque":
            tid=t.id

    bak=bank.objects.filter(Q(vouchertype=vid)|Q (vouchertype=pid)).filter(transactiontype=tid).filter(ledger=uid)
    back=bak
    for  back in back:
        b=back.amount.amount
        sum=sum+b
    return render(request,'chequeprinting.html',{'bank':bak,'sum':sum})


def voucher(request,id):
    bak=bank.objects.get(id=id)
    uid=bak.amount.id
    if contra.objects.filter(amount=uid).exists():
        con=contra.objects.get(amount=uid)
        led=ledger.objects.all()     
        return render(request,'voucher.html',{'bak':bak,'con':con,'led':led})
       
    elif payment.objects.filter(amount=uid).exists():
         con=payment.objects.get(amount=uid)
         led=ledger.objects.all()
         return render(request,'payment.html',{'bak':bak,'con':con,'led':led})
    else:
        con=receipt.objects.get(amount=uid)
        led=ledger.objects.all()
        return render(request,'receipt.html',{'bak':bak,'con':con,'led':led})

def updatepayment(request,id):
    if request.method=="POST":
        bak=bank.objects.get(id=id)
        uid=bak.ledger.id
        led=ledger.objects.get(id=uid)
        nid=led.id
        bid=bak.id
        pid=bak.date.id
        aid=bak.amount.id
        accot=account.objects.get(id=pid)
        part=Particulars.objects.get(id=aid)
        accod=request.POST.get('accot')
        partd=request.POST.get('part')
        ledaccount=ledger.objects.get(name=accod)
        ledparticulars=ledger.objects.get(name=partd)

        if partd is None:
            messages.info(request,'Enter the particulars')
            return redirect('voucher', bid)       
        elif accod is None: 
            messages.info(request,'Enter the account')
            return redirect('voucher', bid) 
        elif request.POST.get('amount') is None:
            messages.info(request,'Enter the amount')
            return redirect('voucher', bid)

        elif contra.objects.filter(amount=aid).exists():
            con=contra.objects.get(amount=aid)
            cond=contra.objects.get(id=con.id)
            part.amount=request.POST.get('amount')

            accot.account=ledaccount
            date=request.POST.get('date')
            accot.date=date
            
            part.particualrs=ledparticulars
            accot.save()
            part.save()
            amountid=part
            dateid=accot
            cond.date=dateid
            cond.amount=amountid
            cond.ledger=ledparticulars
            cond.save()
            bak.ledger=ledparticulars
            bak.amount=part
            bak.date=accot
            bak.save()
            return redirect('bankall', id)

        else:
            uid=bak.ledger.id
            led=ledger.objects.get(id=uid)
            nid=led.id
            pay=payment.objects.get(amount=aid)
            payd=payment.objects.get(id=pay.id)
            part.amount=request.POST.get('amount')
            date=request.POST.get('date')
            accot.account=ledaccount
            part.particualrs=ledparticulars
            accot.date=date
            accot.save()
            part.save()
            dateid=accot
            amountid=part
            payd.ledger=ledaccount
            payd.date=dateid
            payd.amount=amountid
            payd.save()
            bak.ledger=ledaccount
            bak.amount=part
            bak.date=accot
            bak.save()
        return redirect('bankall', id)
    return redirect('voucher', id)


def bankall(request,id):
    bak=bank.objects.get(id=id)
    tran=transactiontype.objects.all()
    return render(request,'bank.html',{'bak':bak,'tran':tran})

def savebank(request,id):
    bak=bank.objects.get(id=id)
    uid=bak.ledger.id
    led=ledger.objects.get(id=uid)
    pd=led.id

    if request.method=="POST":
        bak.instno=request.POST.get('instno')
        bak.instdate=request.POST.get('date')
        transaction=request.POST.get('transaction')
        trans=transactiontype.objects.get(transactiontype=transaction)
        bak.transactiontype=trans
        bak.save()
        return redirect('home')

def changecontra(request,id):
    bak=bank.objects.get(id=id)
    v=Vouchertype.objects.all()
    for v in v:
        if v.vouchertype=='Contra':
            uid=v.id
    type=Vouchertype.objects.get(id=uid)
    led=ledger.objects.all()
    con=contra.objects.all().last()
    try:
        if contra.objects.filter(amount=bak.amount).exists():
            new=contra.objects.get(amount=bak.amount)
            no=new.no 
        else:
            no=con.no+1 
    except:
        no=1   
    return render(request,'convertcontra.html',{'bak':bak,'type':type,'led':led,'con':no})

def changepayment(request,id):
    bak=bank.objects.get(id=id)
    v=Vouchertype.objects.all()
    for v in v:
        if v.vouchertype=='Payment':
            uid=v.id
        
    type=Vouchertype.objects.get(id=uid)
    led=ledger.objects.all()
    con=payment.objects.all().last()
    try:
        if payment.objects.filter(amount=bak.amount).exists():
            new=payment.objects.get(amount=bak.amount)
            no=new.no 
        else:
            no=con.no+1
    except:
        no=1
    print(no)
       
    return render(request,'convertcontra.html',{'bak':bak,'type':type,'led':led,'con':no})

def changerecipt(request,id):
    bak=bank.objects.get(id=id)
    v=Vouchertype.objects.all()

    for v in v:
        if v.vouchertype=='Receipt':
            uid=v.id
        
    type=Vouchertype.objects.get(id=uid)
    led=ledger.objects.all()
    con=receipt.objects.all().last()
    try:
        if receipt.objects.filter(amount=bak.amount).exists():
           new=receipt.objects.get(amount=bak.amount)
           no=new.no
        else:
           no=con.no+1
    except:
        no=1   
    return render(request,'convertcontra.html',{'bak':bak,'type':type,'led':led,'con':no})

def updateconvertpayment(request,id):
     bak=bank.objects.get(id=id)
     if contra.objects.filter(amount=bak.amount).exists():
        return redirect('updatepayment',id)
     elif payment.objects.filter(amount=bak.amount).exists():
        p=payment.objects.get(amount=bak.amount)
        p.delete()
        try:
            con=contra.objects.all().last()
            no=con.no+1
        except:
            no=1   
        bak=bank.objects.get(id=id)
        bid=bak.id
        pid=bak.date.id
        aid=bak.amount.id                
        accot=account.objects.get(id=pid)
        part=Particulars.objects.get(id=aid)
        accod=request.POST.get('accot')
        partd=request.POST.get('part')
        voucher=request.POST.get('voucher')
        print(voucher)
        v=Vouchertype.objects.get(id=voucher)
        ledaccount=ledger.objects.get(name=accod)
        ledparticulars=ledger.objects.get(name=partd)
        date=request.POST.get('date')
        part.amount=request.POST.get('amount')
        accot.account=ledaccount
        accot.date=date
        part.particualrs=ledparticulars
        accot.save()
        part.save()
        amountid=part
        dateid=accot
        con=contra(vouchertype=v,ledger=ledparticulars,no=no,amount=amountid,date=dateid)
        con.save()
        bak.vouchertype=v
        bak.ledger=ledparticulars
        bak.amount=part
        bak.date=accot
        bak.save()
        return redirect('bankall', id)

     else:
        p=receipt.objects.get(amount=bak.amount)
        p.delete()
        try:
            con=contra.objects.all().last()
            no=con.no+1
        except:
            no=1   
        bak=bank.objects.get(id=id)
        bid=bak.id
        pid=bak.date.id
        aid=bak.amount.id                
        accot=account.objects.get(id=pid)
        part=Particulars.objects.get(id=aid)
        accod=request.POST.get('accot')
        partd=request.POST.get('part')
        voucher=request.POST.get('voucher')
        print(voucher)
        v=Vouchertype.objects.get(id=voucher)
        ledaccount=ledger.objects.get(name=accod)
        ledparticulars=ledger.objects.get(name=partd)
        date=request.POST.get('date')
        part.amount=request.POST.get('amount')
        accot.account=ledaccount
        accot.date=date
        part.particualrs=ledparticulars
        accot.save()
        part.save()
        amountid=part
        dateid=accot
        con=contra(vouchertype=v,ledger=ledaccount,no=no,amount=amountid,date=dateid)
        con.save()
        bak.vouchertype=v
        bak.ledger=ledaccount
        bak.amount=part
        bak.date=accot
        bak.save()
        return redirect('bankall', id)



def updateconvertcontra(request,id):
     bak=bank.objects.get(id=id)
     if payment.objects.filter(amount=bak.amount).exists():
        return redirect('updatepayment',id)
     elif contra.objects.filter(amount=bak.amount).exists():
        p=contra.objects.get(amount=bak.amount)
        p.delete()
        try:
            con=payment.objects.all().last()
            no=con.no+1   
        except:
            no=1
        bak=bank.objects.get(id=id) 
        
        pid=bak.date.id
        aid=bak.amount.id      
        accot=account.objects.get(id=pid)
        part=Particulars.objects.get(id=aid)
        voucher=request.POST.get('voucher')  
        v=Vouchertype.objects.get(id=voucher) 
        accod=request.POST.get('accot')
        partd=request.POST.get('part')
        
        
        ledaccount=ledger.objects.get(name=accod)
        ledparticulars=ledger.objects.get(name=partd)
        date=request.POST.get('date')
        part.amount=request.POST.get('amount')
        accot.account=ledaccount
        accot.date=date
        part.particualrs=ledparticulars
        accot.save()
        part.save()
        amountid=part
        dateid=accot       
        con=payment(vouchertype=v,ledger=ledaccount,no=no,amount=amountid,date=dateid)
        con.save()
        bak.vouchertype=v
        bak.ledger=ledaccount
        bak.amount=part
        bak.date=accot
        bak.save()
        return redirect('bankall', id)
     else:
        p=receipt.objects.get(amount=bak.amount)
        p.delete()
        try:
            con=contra.objects.all().last()
            no=con.no+1
        except:
            no=1   
        bak=bank.objects.get(id=id)
        bid=bak.id
        pid=bak.date.id
        aid=bak.amount.id                
        accot=account.objects.get(id=pid)
        part=Particulars.objects.get(id=aid)
        accod=request.POST.get('accot')
        partd=request.POST.get('part')
        voucher=request.POST.get('voucher')
        print(voucher)
        v=Vouchertype.objects.get(id=voucher)
        ledaccount=ledger.objects.get(name=accod)
        ledparticulars=ledger.objects.get(name=partd)
        date=request.POST.get('date')
        part.amount=request.POST.get('amount')
        accot.account=ledaccount
        accot.date=date
        part.particualrs=ledparticulars
        accot.save()
        part.save()
        amountid=part
        dateid=accot
        con=payment(vouchertype=v,ledger=ledaccount,no=no,amount=amountid,date=dateid)
        con.save()
        bak.vouchertype=v
        bak.ledger=ledaccount
        bak.amount=part
        bak.date=accot
        bak.save()
        return redirect('bankall', id)

def updateconvertreceipt(request,id):
    bak=bank.objects.get(id=id)
    if payment.objects.filter(amount=bak.amount.id).exists():
        p=payment.objects.get(amount=bak.amount.id)
        p.delete()
        if request.method=="POST":
            pid=bak.date.id
            aid=bak.amount.id   
            accot=account.objects.get(id=pid)
            part=Particulars.objects.get(id=aid)
            accod=request.POST.get('accot')
            partd=request.POST.get('part')
            vid=request.POST.get('voucher')
            ledaccount=ledger.objects.get(name=accod)
            ledparticulars=ledger.objects.get(name=partd)
            date=request.POST.get('date')
            part.amount=request.POST.get('amount')
            accot.account=ledaccount
            accot.date=date
            part.particualrs=ledparticulars
            accot.save()
            part.save()
            amountid=part
            dateid=accot            
            voucher=request.POST.get('voucher')  
            v=Vouchertype.objects.get(id=voucher) 
            try:
                recpt=receipt.objects.all().last()
                no=recpt.no+1
            except:
                no=1
            rec=receipt(vouchertype=v,ledger=ledaccount,no=no,date=dateid,amount=amountid)
            rec.save()
            bak.vouchertype=v
            bak.save()
            
            return redirect('bankall',id)
        
    else:
        p=contra.objects.get(amount=bak.amount.id)
        p.delete()
        if request.method=="POST":
            pid=bak.date.id
            aid=bak.amount.id   
            accot=account.objects.get(id=pid)
            part=Particulars.objects.get(id=aid)
            accod=request.POST.get('accot')
            partd=request.POST.get('part')
            vid=request.POST.get('voucher')
            v=Vouchertype.objects.all()
            for v in v:
                if v.vouchertype == vid:
                   zid=v.id
            ledaccount=ledger.objects.get(name=accod)
            ledparticulars=ledger.objects.get(name=partd)
            date=request.POST.get('date')
            part.amount=request.POST.get('amount')
            accot.account=ledaccount
            accot.date=date
            part.particualrs=ledparticulars
            accot.save()
            part.save()
            amountid=part
            dateid=accot
            transaction=bak.transactiontype.id
           
            try:
                recpt=receipt.objects.all().last()
                no=recpt.no+1
            except:
                no=1
            rec=receipt(ledger=ledaccount,vouchertype=zid,no=no,date=dateid,amount=amountid)
            rec.save()
            bak.vouchertype=zid
            bak.save()
            
            return redirect('bankall',id)
    return redirect('voucher',id)

def receiptbank(request,id):
    bak=bank.objects.get(id=id)
    tran=transactiontype.objects.all()
    return render(request,'bankreceipt.html',{'bak':bak,'tran':tran})

def savereceiptbank(request,id):

    if request.method=="POST":
        bak=bank.objects.get(id=id)
        ledgid=bak.ledger.id
        accot=bak.date.id
        particulars=bak.amount.id
        led=ledger.objects.get(id=ledgid)
        acc=account.objects.get(id=accot)
        par=Particulars.objects.get(id=particulars)
        
        instno=request.POST.get('instno')
        instdate=request.POST.get('date')
        transaction=request.POST.get('transaction')
        trans=transactiontype.objects.get(transactiontype=transaction)
        rec=bank(ledger=led,date=acc,amount=par,instno=instno,instdate=instdate,transactiontype=trans)
        bak=bank.objects.get(id=id)
        bak.delete()
        rec.save()

        return redirect('home')

def instrument(request,id):
    v=Vouchertype.objects.all()
    for v in v:
        if v.vouchertype=="Contra":
            vid=v.id
        elif v.vouchertype=="Payment":
            pid=v.id
        else:
            pass

    t=transactiontype.objects.all()
    for t in t:
        if t.transactiontype=="Cheque":
            tid=t.id
    sum=0
    bak=bank.objects.filter(Q(vouchertype=vid)|Q (vouchertype=pid)).filter(transactiontype=tid).filter(ledger=id)
    back=bak
    con=contra.objects.all()
    pay=payment.objects.all()

    for  back in back:
        b=back.amount.amount
        sum=sum+b
    return render(request,'instrument.html',{'bank':bak,'sum':sum,'con':con,'pay':pay})

            
def monthlysummary(request, id):
    trans=Vouchertype.objects.all()
    todays_date = datetime.date.today()
    for t in trans:
        if t.vouchertype=="Receipt":
            tid=t.id
    a=bank.objects.filter(ledger=id).values_list('id','instdate').filter(vouchertype=tid)
    print(a)
    b=dict(a)
    
    v=Vouchertype.objects.all()
    for v in v:
        if v.vouchertype=="Contra":
            vid=v.id
        elif v.vouchertype=="Payment":
            pid=v.id
        else:
            pass
    z=transactiontype.objects.all()
    for z in z:
        if z.transactiontype=="Cheque":
            zid=z.id
    new=bank.objects.filter(ledger=id).values_list('id','instdate').filter(Q(vouchertype=vid)|Q (vouchertype=pid)).filter(transactiontype=zid)
    newb=dict(new)
    newamount=bank.objects.filter(ledger=id).values('instdate','amount').filter(Q(vouchertype=vid)|Q (vouchertype=pid)).filter(transactiontype=zid)
    newtotal={}
    for i in range(1,13):
         newj=0
         newtotal[i]=0
         for course in newamount:
            if i==(course['instdate'].month):
                if (course['instdate'])>=todays_date:
                    e=course['amount']
                    par=Particulars.objects.get(id=e)
                    newj=newj+par.amount
                    newtotal[i]=newj
                # elif (course['instdate'].day)>=todays_date.day:
                #     e=course['amount']
                #     par=Particulars.objects.get(id=e)
                #     newj=newj+par.amount
                #     newtotal[i]=newj
                # else:
                #     pass
    newmonth={}
    for i in range(1,13):
        newjan=0
        newmonth[i]=0
        for keys, values in newb.items():
            if i==values.month:
                if values >= todays_date:
                    newjan=newjan+1
                    newmonth[i]=newjan
                # elif values.day>=todays_date.day:
                #     newjan=newjan+1
                #     newmonth[i]=newjan
                # else:
                #     pass
    
    todays_date = datetime.date.today()
    fiscalyear.setup_fiscal_calendar(start_month=4)
    fy = FiscalYear.current()
    current_fiscal_year = FiscalYear.current()
    # d = datetime.datetime(current_fiscal_year.start.year, current_fiscal_year.start.month, current_fiscal_year.start.day)
    # for m in range(0, 12):
    #     next_month_start = d + relativedelta.relativedelta(months=m, day=1)
    #     print(next_month_start.strftime('%Y-%m-%d'))
    month={}
 
    print(todays_date.day)
    
    for i in range(1,13):   
        jan=0
        month[i]=0
        for keys, values in b.items():
            if i==values.month:
                if values >= todays_date:
                    jan=jan+1
                    month[i]=jan
                # elif values.day>=todays_date.day:
                #     jan=jan+1
                #     month[i]=jan
                # else:
                #     pass

    amount=bank.objects.filter(ledger=id).values('instdate','amount').filter(vouchertype=tid)
    total={}
 
    for i in range(1,13):
        j=0
        total[i]=0
        for course in amount:
            if i==(course['instdate'].month):
                if (course['instdate'])>=todays_date:
                    e=course['amount']
                    par=Particulars.objects.get(id=e)
                    j=j+par.amount
                    total[i]=j
                # elif (course['instdate'].day)>=todays_date.day:
                #     e=course['amount']
                #     par=Particulars.objects.get(id=e)
                #     j=j+par.amount
                #     total[i]=j
                # else:
                #     pass

    fiscalyear.setup_fiscal_calendar(start_month=4)
    fy = FiscalYear.current()
    
    
    current_fiscal_year = FiscalYear.current()
    
    d = datetime.datetime(current_fiscal_year.start.year, current_fiscal_year.start.month, current_fiscal_year.start.day)
    f=datetime.datetime(current_fiscal_year.end.year, current_fiscal_year.end.month, current_fiscal_year.end.day)
    next_month_start = d + relativedelta.relativedelta(months=0, day=1)
    s=next_month_start.strftime("%d %b, %Y")
    new=f.strftime("%d %b, %Y")

    bak=bank.objects.filter(ledger=id)

    return render(request,'montlysummary.html',{'month':month,'total':total,'bak':bak,'id':id,'s':s,'new':new,'newmonth':newmonth,'newtotal':newtotal})

def getjune(request,id):
    fiscalyear.setup_fiscal_calendar(start_month=4)
    fy = FiscalYear.current()
    current_fiscal_year = FiscalYear.current()
    todays_date = datetime.date.today()
    d = datetime.datetime(current_fiscal_year.start.year, current_fiscal_year.start.month, current_fiscal_year.start.day)
    for m in range(2, 3):
        for n in range(2,3):
            next_month_start = d + relativedelta.relativedelta(months=m, day=1)
            next_month_end = d + relativedelta.relativedelta(months=n, day=30)
        
            trans=Vouchertype.objects.all()
            for t in trans:
                if t.vouchertype=="Receipt":
                    tid=t.id 
                    
            rec=bank.objects.filter(instdate__gte=next_month_start,instdate__lte=next_month_end,ledger=id).filter(vouchertype=tid)
            print(rec)
    return render(request,'receiptbank.html')

def getjuly(request,id):
    fiscalyear.setup_fiscal_calendar(start_month=4)
    fy = FiscalYear.current()

    current_fiscal_year = FiscalYear.current()
    d = datetime.datetime(current_fiscal_year.start.year, current_fiscal_year.start.month, current_fiscal_year.start.day)
    todays_date = datetime.date.today()
    for m in range(3, 4):
        for n in range(3,4):
            next_month_start = d + relativedelta.relativedelta(months=m, day=1)
            next_month_end = d + relativedelta.relativedelta(months=n, day=31)
            print(next_month_end)
            trans=Vouchertype.objects.all()
            for t in trans:
                if t.vouchertype=="Receipt":
                    tid=t.id 
            rec=bank.objects.filter(instdate__gte=next_month_start,instdate__lte=next_month_end,ledger=id)
            print(rec)
            
    return render(request,'receiptbank.html',{'rec':rec})


def editreceipt(request,id):

    if request.method=="POST":
        bak=bank.objects.get(id=id)
        uid=bak.ledger.id
        led=ledger.objects.get(id=uid)
        nid=led.id
        bid=bak.id
        pid=bak.date.id
        aid=bak.amount.id
        accot=account.objects.get(id=pid)
        part=Particulars.objects.get(id=aid)
        accod=request.POST.get('accot')
        partd=request.POST.get('part')
        ledaccount=ledger.objects.get(name=accod)
        ledparticulars=ledger.objects.get(name=partd)

        if partd is None:
            messages.info(request,'Enter the particulars')
            return redirect('voucher', bid)       
        elif accod is None: 
            messages.info(request,'Enter the account')
            return redirect('voucher', bid) 
        elif request.POST.get('amount') is None:
            messages.info(request,'Enter the amount')
            return redirect('voucher', bid)

        elif receipt.objects.filter(amount=aid).exists():
            con=receipt.objects.get(amount=aid)
            cond=receipt.objects.get(id=con.id)
            part.amount=request.POST.get('amount')

            accot.account=ledaccount
            date=request.POST.get('date')
            accot.date=date
            
            part.particualrs=ledparticulars
            accot.save()
            part.save()
            amountid=part
            dateid=accot
            cond.date=dateid
            cond.amount=amountid
            cond.ledger=ledaccount
            cond.save()
            bak.ledger=ledaccount
            bak.amount=part
            bak.date=accot
            bak.save()
            return redirect('bankall', id)



def getaugust(request,id):
    fiscalyear.setup_fiscal_calendar(start_month=4)
    fy = FiscalYear.current()
    print(fy)
    current_fiscal_year = FiscalYear.current()
    d = datetime.datetime(current_fiscal_year.start.year, current_fiscal_year.start.month, current_fiscal_year.start.day)
    todays_date = datetime.date.today()
    for m in range(4, 5):
        for n in range(4,5):
            next_month_start = d + relativedelta.relativedelta(months=m, day=1)
            next_month_end = d + relativedelta.relativedelta(months=n, day=31)
            print(next_month_end)
            print(todays_date)
            trans=Vouchertype.objects.all()
            for t in trans:
                if t.vouchertype=="Receipt":
                    tid=t.id 
            rec=bank.objects.filter(instdate__gte=next_month_start,instdate__lte=next_month_end,ledger=id)
            print(rec)
            
    return render(request,'receiptbank.html',{'rec':rec})

def getseptember(request,id):
    fiscalyear.setup_fiscal_calendar(start_month=4)
    fy = FiscalYear.current()

    current_fiscal_year = FiscalYear.current()
    d = datetime.datetime(current_fiscal_year.start.year, current_fiscal_year.start.month, current_fiscal_year.start.day)
    todays_date = datetime.date.today()
    for m in range(5, 6):
        for n in range(5,6):
            next_month_start = d + relativedelta.relativedelta(months=m, day=1)
            next_month_end = d + relativedelta.relativedelta(months=n, day=31)
            print(next_month_end)
            trans=Vouchertype.objects.all()
            for t in trans:
                if t.vouchertype=="Receipt":
                    tid=t.id 
            rec=bank.objects.filter(instdate__gte=next_month_start,instdate__lte=next_month_end,ledger=id)
            print(rec)
            
    return render(request,'receiptbank.html',{'rec':rec})


def getoctober(request,id):
    fiscalyear.setup_fiscal_calendar(start_month=4)
    fy = FiscalYear.current()

    current_fiscal_year = FiscalYear.current()
    d = datetime.datetime(current_fiscal_year.start.year, current_fiscal_year.start.month, current_fiscal_year.start.day)
    todays_date = datetime.date.today()
    for m in range(6, 7):
        for n in range(6,7):
            next_month_start = d + relativedelta.relativedelta(months=m, day=1)
            next_month_end = d + relativedelta.relativedelta(months=n, day=31)
            print(next_month_end)
            trans=Vouchertype.objects.all()
            for t in trans:
                if t.vouchertype=="Receipt":
                    tid=t.id 
            rec=bank.objects.filter(instdate__gte=next_month_start,instdate__lte=next_month_end,ledger=id)
            print(rec)
            
    return render(request,'receiptbank.html',{'rec':rec})            
        
def getnovember(request,id):
    fiscalyear.setup_fiscal_calendar(start_month=4)
    fy = FiscalYear.current()

    current_fiscal_year = FiscalYear.current()
    d = datetime.datetime(current_fiscal_year.start.year, current_fiscal_year.start.month, current_fiscal_year.start.day)
    todays_date = datetime.date.today()
    for m in range(7, 8):
        for n in range(7,8):
            next_month_start = d + relativedelta.relativedelta(months=m, day=1)
            next_month_end = d + relativedelta.relativedelta(months=n, day=31)
            print(next_month_end)
            trans=Vouchertype.objects.all()
            for t in trans:
                if t.vouchertype=="Receipt":
                    tid=t.id 
            rec=bank.objects.filter(instdate__gte=next_month_start,instdate__lte=next_month_end,ledger=id)
            print(rec)
            
    return render(request,'receiptbank.html',{'rec':rec})
            


def getdecember(request,id):
    fiscalyear.setup_fiscal_calendar(start_month=4)
    fy = FiscalYear.current()

    current_fiscal_year = FiscalYear.current()
    d = datetime.datetime(current_fiscal_year.start.year, current_fiscal_year.start.month, current_fiscal_year.start.day)
    todays_date = datetime.date.today()
    for m in range(7, 8):
        for n in range(7,8):
            next_month_start = d + relativedelta.relativedelta(months=m, day=1)
            next_month_end = d + relativedelta.relativedelta(months=n, day=31)
            print(next_month_end)
            trans=Vouchertype.objects.all()
            for t in trans:
                if t.vouchertype=="Receipt":
                    tid=t.id 
            rec=bank.objects.filter(instdate__gte=next_month_start,instdate__lte=next_month_end,ledger=id)
            print(rec)
            
    return render(request,'receiptbank.html',{'rec':rec})


def getjanuary(request,id):
    fiscalyear.setup_fiscal_calendar(start_month=1)
    fy = FiscalYear.current()

    current_fiscal_year = FiscalYear.current()
    d = datetime.datetime(current_fiscal_year.start.year, current_fiscal_year.start.month, current_fiscal_year.start.day)
    todays_date = datetime.date.today()
    for m in range(0, 1):
        for n in range(0, 1):
            next_month_start = d + relativedelta.relativedelta(months=m, day=1)
            next_month_end = d + relativedelta.relativedelta(months=n, day=31)
            print(next_month_end)
            trans=Vouchertype.objects.all()
            for t in trans:
                if t.vouchertype=="Receipt":
                    tid=t.id 
            rec=bank.objects.filter(instdate__gte=next_month_start,instdate__lte=next_month_end,ledger=id)
            print(rec)
            
    return render(request,'receiptbank.html',{'rec':rec})


def getfebruary(request,id):
    fiscalyear.setup_fiscal_calendar(start_month=2)
    fy = FiscalYear.current()

    current_fiscal_year = FiscalYear.current()
    d = datetime.datetime(current_fiscal_year.start.year, current_fiscal_year.start.month, current_fiscal_year.start.day)
    todays_date = datetime.date.today()
    for m in range(0, 1):
        for n in range(0,1):
            next_month_start = d + relativedelta.relativedelta(months=m, day=1)
            next_month_end = d + relativedelta.relativedelta(months=n, day=31)
            print(next_month_end)
            trans=Vouchertype.objects.all()
            for t in trans:
                if t.vouchertype=="Receipt":
                    tid=t.id 
            rec=bank.objects.filter(instdate__gte=next_month_start,instdate__lte=next_month_end,ledger=id)
            print(rec)
            
    return render(request,'receiptbank.html',{'rec':rec})

def getmarch(request,id):
    fiscalyear.setup_fiscal_calendar(start_month=3)
    fy = FiscalYear.current()

    current_fiscal_year = FiscalYear.current()
    d = datetime.datetime(current_fiscal_year.start.year, current_fiscal_year.start.month, current_fiscal_year.start.day)
    todays_date = datetime.date.today()
    for m in range(0, 1):
        for n in range(0,1):
            next_month_start = d + relativedelta.relativedelta(months=m, day=1)
            next_month_end = d + relativedelta.relativedelta(months=n, day=31)
            print(next_month_end)
            trans=Vouchertype.objects.all()
            for t in trans:
                if t.vouchertype=="Receipt":
                    tid=t.id 
            rec=bank.objects.filter(instdate__gte=next_month_start,instdate__lte=next_month_end,ledger=id)
            print(rec)
            
    return render(request,'receiptbank.html',{'rec':rec})

def getapril(request,id):
    fiscalyear.setup_fiscal_calendar(start_month=4)
    fy = FiscalYear.current()

    current_fiscal_year = FiscalYear.current()
    d = datetime.datetime(current_fiscal_year.start.year, current_fiscal_year.start.month, current_fiscal_year.start.day)
    todays_date = datetime.date.today()
    for m in range(0, 1):
        for n in range(0,1):
            next_month_start = d + relativedelta.relativedelta(months=m, day=1)
            next_month_end = d + relativedelta.relativedelta(months=n, day=31)
            print(next_month_end)
            trans=Vouchertype.objects.all()
            for t in trans:
                if t.vouchertype=="Receipt":
                    tid=t.id 
            rec=bank.objects.filter(instdate__gte=next_month_start,instdate__lte=next_month_end,ledger=id)
            print(rec)
            
    return render(request,'receiptbank.html',{'rec':rec})

def getmay(request,id):
    fiscalyear.setup_fiscal_calendar(start_month=4)
    fy = FiscalYear.current()

    current_fiscal_year = FiscalYear.current()
    d = datetime.datetime(current_fiscal_year.start.year, current_fiscal_year.start.month, current_fiscal_year.start.day)
    todays_date = datetime.date.today()
    for m in range(5, 6):
        for n in range(5,6):
            next_month_start = d + relativedelta.relativedelta(months=m, day=1)
            next_month_end = d + relativedelta.relativedelta(months=n, day=31)
            print(next_month_end)
            trans=Vouchertype.objects.all()
            for t in trans:
                if t.vouchertype=="Receipt":
                    tid=t.id 
            rec=bank.objects.filter(instdate__gte=next_month_start,instdate__lte=next_month_end,ledger=id)
            print(rec)
            
    return render(request,'receiptbank.html',{'rec':rec})