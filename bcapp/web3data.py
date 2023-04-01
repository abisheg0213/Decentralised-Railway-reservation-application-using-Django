from solcx import compile_source 
from web3 import Web3
import datetime
con_instance=""
w3=Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545'))
railway=""
a=""
tx_recipt=""
def compile():
    global railway
    global a
    global tx_recipt
    compiled_sol=compile_source(
    '''
    pragma solidity ^0.8.14;
    contract railway
    {
        uint ticket_id=1020;
        uint refund_id=1;
        uint [20] nonac;
        uint [15] public ac;
        uint public totalincome;
        uint nonac_rate=150;
        uint ac_rate=450;
        uint nonac_avail=20;
        uint ac_avail=15;
        address[] users;
        uint[] btk;
        struct ticket_booked
        {
            address p;
            uint coach;
            uint[] seat_no;
            uint total_amount_spend;
            uint time;
        }
        struct refund
        {
            uint t_id;
            uint refund_amount;
            uint time;
        }
        mapping(uint => ticket_booked) public tb;
        mapping(uint => refund) public refunds;
        function setval() private{
            for(uint i=0;i<20;i++)
            {
                nonac[i]=0;
            }
            for(uint i=0;i<15;i++)
            {
                ac[i]=0;
            }
        }
        constructor()
        {
            setval();
        }
        function availablity(uint coach,uint y) public view returns(bool)
        {
            bool res=false;
            if(coach==101)
            {
                if(ac_avail>=y)
                {
                    res=true;
                }
            }
            if(coach==102)
            {
                if(nonac_avail>=y)
                {
                    res=true;
                }
            }
            return res;
        }
        function reg_user() public
        {
            users.push(msg.sender);
        }
        function ret_current_seat(uint c) private returns(uint)
        {
            uint t;
            if(c==102)
            {
                for(uint i=0;i<20;i++)
                {
                    if(nonac[i]==0)
                    {
                        t=i;
                        break;
                    }
                }
            }
            if(c==101)
            {
                for(uint i=0;i<15;i++)
                {
                    if(ac[i]==0)
                    {
                        t=i;
                        break;
                    }
                }
            }
            return t;
        }
        function vaild_user(address r) private returns(bool)
        {
            uint y=0;
            bool avail;
            for(uint i=0;i<users.length;i++)
            {
                // v=i;
                if(users[i]==r)
                {
                    avail=true;
                    y=1;
                }
            }
            if (y==0)
            {
                avail=false;
            }
            return avail;
        }
        modifier val_user(address k)
        {
            require(vaild_user(k)==true);
            _;
        }
        function book_tickets(uint c,uint no) public val_user(msg.sender)
        {
            for(uint i=0;i<btk.length;i++)
            {
                btk.pop();
            }
            uint ty=ret_current_seat(c);
            if(c==102)
            {
                for(uint u=0;u<no;u++)
                {
                    btk.push(ty+u);
                    nonac[ty+u]=1;
                }
                totalincome+=(no*nonac_rate);
                tb[ticket_id]=(ticket_booked(msg.sender,c,btk,no*nonac_rate,block.timestamp));
                ticket_id++;
                nonac_avail-=no;
            }
            if(c==101)
            {
                for(uint u=0;u<no;u++)
                {
                    btk.push(ty+u);
                    ac[ty+u]=1;
                }
                totalincome+=(no*ac_rate);
                tb[ticket_id]=(ticket_booked(msg.sender,c,btk,no*ac_rate,block.timestamp));
                ticket_id++;
                ac_avail-=no;
            }
        }
        function cancel_ticket(uint id,uint c) public
        {
            uint tp=tb[id].total_amount_spend;
            uint am=tp-225;
            refunds[refund_id]=refund(id,am,block.timestamp);
            totalincome=totalincome-am;
            if(c==101)
            {
            for(uint i=0;i<tb[id].seat_no.length;i++)
            {
                ac[tb[id].seat_no[i]]=0;
            }
            ac_avail+=(tb[id].total_amount_spend/450);
            }
            if(c==102)
            {
            for(uint i=0;i<tb[id].seat_no.length;i++)
            {
                nonac[tb[id].seat_no[i]]=0;
            }
            nonac_avail+=(tb[id].total_amount_spend/150);
            }
        }
        function checkav(uint c) view public returns(uint)
        {
            if(c==101)
            {
                return ac_avail;
            }
            else
            {
                return nonac_avail;
            }
        }
    }
    '''
    ,output_values=['bin','abi']
    )
   
    contract_id,contract_interface=compiled_sol.popitem()
    a=contract_interface['abi']
    b=contract_interface['bin']
    railway=w3.eth.contract(abi=a,bytecode=b)
def cons():
    global tx_recipt
    tx=railway.constructor().buildTransaction(
    {
        'from':"0x51dE4Dea217B52D88aB41652C0A53F9D39e89524",
        'nonce':w3.eth.getTransactionCount("0x51dE4Dea217B52D88aB41652C0A53F9D39e89524"),
        'gasPrice':w3.eth.gas_price
    }
    )
    p="0x992963ae8e4c108b5afdca2d02b6f7db8c899a4ec56146893d817a5bb6564760"
    signed_tx=w3.eth.account.sign_transaction(tx,private_key=p)
    tx_hash=w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_recipt=w3.eth.wait_for_transaction_receipt(tx_hash)
def create_inst():
    global con_instance
    global tx_recipt
    print(tx_recipt.contractAddress)
    print(a)
    con_instance=w3.eth.contract(address=tx_recipt.contractAddress,abi=a)
def book_ticket(address,private,c,no):
    tx=con_instance.functions.book_tickets(c,no).buildTransaction(
    {
        'from':address,
        'nonce':w3.eth.getTransactionCount(address),
        'gasPrice':w3.eth.gas_price
    }
    )
    signed_tx=w3.eth.account.sign_transaction(tx,private_key=private)
    tx_hash=w3.eth.send_raw_transaction(signed_tx.rawTransaction)
def canc_ticket(address,private,id,c):
    tx=con_instance.functions.cancel_ticket(id,c).buildTransaction(
    {
        'from':address,
        'nonce':w3.eth.getTransactionCount(address),
        'gasPrice':w3.eth.gas_price
    }
    )
    signed_tx=w3.eth.account.sign_transaction(tx,private_key=private)
    tx_hash=w3.eth.send_raw_transaction(signed_tx.rawTransaction)
def view_tavail(c,n):
    output=con_instance.functions.availablity(c,n).call()
    return output
def register_user(address,p_key):
    tx=con_instance.functions.reg_user().buildTransaction(
    {
        'from':address,
        'nonce':w3.eth.getTransactionCount(address),
        'gasPrice':w3.eth.gas_price
    }
    )
    signed_tx=w3.eth.account.sign_transaction(tx,private_key=p_key)
    tx_hash=w3.eth.send_raw_transaction(signed_tx.rawTransaction)
def log_booked_tc(i):
    l=con_instance.functions.tb(1020).call()
    res=[]
    res.append(l[0])
    res.append(l[1])
    res.append(l[2])
    date_time = datetime.datetime.fromtimestamp(l[3])
    d = date_time.strftime("%d/%m/%Y time:  %H:%M:%S")
    res.append(d)
    return res
def log_canceled_tc(i):
    l=con_instance.functions.refunds(i).call()
    res=[]
    res.append(l[0])
    res.append(l[1])
    date_time = datetime.datetime.fromtimestamp(l[2])
    d = date_time.strftime("%d/%m/%Y time:  %H:%M:%S")
    res.append(d)
    print(res)
    return res
def call_me_first():
    compile()
    cons()
    create_inst()
def checkavail(cno):
    l=con_instance.functions.checkav(cno).call()
    return l