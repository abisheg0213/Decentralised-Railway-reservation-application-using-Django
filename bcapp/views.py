from django.shortcuts import render
from . import web3data
web3data.call_me_first()
ticketid=1020
refundid=1
accounts={'Account-1':'0x51dE4Dea217B52D88aB41652C0A53F9D39e89524',"Account-2":'0x38490827946ab2846dF2B7f921790d234aABBCFa'}
pvkey={'0x51dE4Dea217B52D88aB41652C0A53F9D39e89524':'0x992963ae8e4c108b5afdca2d02b6f7db8c899a4ec56146893d817a5bb6564760','0x38490827946ab2846dF2B7f921790d234aABBCFa':'0x6309a62ae269af6b1b80165e1547b54d984224d83f5132aad7bd0cc88f42560c'}
# Create your views here.
coach={'AC':101,'NON AC':102}
def display(request):
    return render(request,'index.html')
def d1(request):
    if request.method=="POST":
        a=request.POST['acco']
        d=accounts[a]
        web3data.register_user(d,pvkey[d])
        return render(request,'register.html')
    return render(request,'register.html')
def booktic(request):
    global ticketid
    if request.method=="POST":
        a=request.POST['acco']
        b=request.POST['coach']
        c=int(request.POST['nooftic'])
        web3data.book_ticket(accounts[a],pvkey[accounts[a]],coach[b],c)
        l=web3data.log_booked_tc(ticketid)
        print(l)
        tj=ticketid
        ticketid+=1
        return render(request,'portfolio-details.html',{'notc':c,'data':tj,'ad':l[0][0:10],'coach':l[1],'amount':l[2],'date':l[3]})
    return render(request,'bookticket.html')
def cantic(request):
    global refundid
    if request.method=="POST":
        a=int(request.POST['ticketid'])
        c=request.POST['coach']
        web3data.canc_ticket(accounts['Account-1'],pvkey[accounts['Account-1']],a,coach[c])
        k=web3data.log_canceled_tc(refundid)
        refundid+=1
        return render(request,'cancel_ticket_log.html',{'id':a,'refund':k[1],'date':k[2]})
    return render(request,'canceltickets.html')
def ticket_details(request):
    return render(request,'portfolio-details.html')
def avreq(request):
    if request.method=='POST':
        c=request.POST['coach']
        kp=web3data.checkavail(coach[c])
        return render(request,'av.html',{'c':c,'av':kp})
    return render(request,'availrequest.html')