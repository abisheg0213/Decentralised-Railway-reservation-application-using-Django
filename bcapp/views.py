from django.shortcuts import render
from . import web3data
web3data.call_me_first()
ticketid=1020
refundid=1
accounts={'Account-1':'0x776ec72f4A4F576E94732892dd03346254Ff9A87',"Account-2":'0x69B394439BC471D7235C0f2b12E56A6069ac06A4'}
pvkey={'0x776ec72f4A4F576E94732892dd03346254Ff9A87':'0x0a26f661a093595e709fe5487663f6cbc5a419a249effad9d94359bb606d71f9','0x69B394439BC471D7235C0f2b12E56A6069ac06A4':'0x42043f359caf1e5b94a14fc008da9c8f4477b432aab4329c0a702ca9f2149ca8'}
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