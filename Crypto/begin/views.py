from django.shortcuts import render
from django.http import  HttpResponse
from . import models
from .models import Block,Blockchain,Block2
from django.shortcuts import render,redirect
from django.http import HttpResponse
from passlib.hash import sha256_crypt
import random,passlib
from django.contrib.auth.models import User,auth

from hashlib import sha256


def index(request):
    balance = 0
    if request.user.is_authenticated:
        balance = get_balance(str(request.user))
    return render(request,'index.html',{'balance':balance})

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            message.info(request,'invalid credentials')
            return redirect('login')


    else:

        return render(request,'login.html')

def register(request):
    print("register called")
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name'] 
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            print("username taken")

        else:
            user = User.objects.create_user(username=username,password=password,email=email,first_name=first_name,last_name=last_name)
            user.save()
            return redirect('/')

    else :
        return render(request,'register.html')



def hashing(*args):
    h = sha256()
    hashing_text = ""
    for arg in args:
        hashing_text += str(arg)
    h.update(hashing_text.encode('utf-8'))
    return h.hexdigest()
def createblock(number,data,blockchain):
        nonce = 0
        
        if len(blockchain.chain) != 0:
            previous_hash = hashing(blockchain.chain[-1].previous_hash,blockchain.chain[-1].number,blockchain.chain[-1].data,blockchain.chain[-1].nonce)
        else:
            
            previous_hash = "0" * 64
        num = number
        temphash = hashing(previous_hash,num,data,nonce)
        
        latestblock = Block(number = num,hash = temphash,previous_hash = previous_hash,data = data,nonce = nonce)
        
        
        
        return latestblock

def sendmoney(sender,reciever,amount):

    amount = float(amount)
    userlist = User.objects.all()
    found = False
    for x in userlist:
        if reciever == x.username:
            found = True
        
    if amount > get_balance(sender) and sender != "BANK" :
        print("insufficient balance ")
    elif sender == reciever:
        print("cant transfer balance to self")
    elif amount <= 0:
        print("enter amount greater than 0")
    elif found == False:
        print("reciever is not found in")
    else:

        blockchain = get_blockchain()
        number = len(blockchain.chain) + 1
        data = sender + "-->" + reciever + "-->" + str(amount)
        latestblock = createblock(number,data,blockchain)
        blockchain.mine(latestblock)
        sync_blockchain(blockchain)



    


def get_balance(username):
    balance = 0
    blockchain = get_blockchain()
    for block in blockchain.chain :
        data = block.data.split("-->")
        if len(data) > 2:
            if username == data[0]:
                balance = balance - float(data[2])
            elif username == data[1]:
                balance = balance + float(data[2])
    return balance

def get_blockchain():
    blockchain = Blockchain()
    blocklist = Block.objects.all()
    for blocks in blocklist:
        blockchain.add(blocks)
    return blockchain
def sync_blockchain(blockchain):
    Block.objects.all().delete()
    for block in blockchain.chain:
        block.save()
def test_blockchain():
    blockchain = Blockchain()
    #print("blockchain has been called")
    database = ["hello","how","are","you"]
    num = 0
    for val in database:
        
        nonce = 0
        
        if len(blockchain.chain) != 0:
            previous_hash = hashing(blockchain.chain[-1].previous_hash,blockchain.chain[-1].number,blockchain.chain[-1].data,blockchain.chain[-1].nonce)
        else:
            
            previous_hash = "0" * 64
        num += 1
        temphash = hashing(previous_hash,num,val,nonce)
        
        latestblock = Block(number = num,hash = temphash,previous_hash = previous_hash,data = val,nonce = nonce)
        #print(latestblock)
        
        
        blockchain.mine(latestblock)
    for x in blockchain.chain:
            print(x.previous_hash,"and ",x.hash)
    sync_blockchain(blockchain)

def transaction(request):
    if request.user.is_authenticated:
        currentuser = str(request.user)
        balance = get_balance(currentuser)
        if request.method == "POST":
            reciever = request.POST['reciever']
            amount = request.POST['amount']
            sender = str(request.user)
            sendmoney(sender,reciever,amount)

         
            return redirect('/')
        else:
            return render(request,'transaction.html',{'balance' : balance })
    else:
            return redirect('/login')
def buycrypto(request):
    if request.user.is_authenticated:
        user  = str(request.user)
        balance = get_balance(str(request.user))
        if request.method == "POST":
            amount = request.POST['amount']
            sendmoney("BANK",user,amount)
            return redirect("/")



        else:
            return render(request,'buycrypto.html',{'balance':balance})      
    else:
        return redirect('/login')
def logout(request):
    auth.logout(request)
    return redirect('/')