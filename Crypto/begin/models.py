from django.db import models
from hashlib import sha256
def updatehash(*args):
    hashing_text = ""; h = sha256()
    for arg in args:
        hashing_text += str(arg)
    h.update(hashing_text.encode('utf-8'))
    return h.hexdigest()
def hashing(*args):
    h = sha256()
    hashing_text = ""
    for arg in args:
        hashing_text += str(arg)
    h.update(hashing_text.encode('utf-8'))
    return h.hexdigest()
class Block(models.Model):
    number = models.CharField(max_length = 10)
    hash = models.CharField(max_length = 64)
    previous_hash = models.CharField(max_length = 64)
    data = models.CharField(max_length = 100)
    nonce = models.CharField(max_length = 15)
    



class Block2():
    data = None
    hash = None
    nonce = 0
    previous_hash = "0" * 64
    def __init__(self,data,number=0):
        self.data = data
        self.number = number
    
    def hashing(self):
        
        return updatehash(self.previous_hash,self.number,self.data,self.nonce)

    
class Blockchain():
    difficulty = 2
    def __init__(self,):
        self.chain = []

    def add(self,block):
        #print("add is called for block",block.data)
        self.chain.append(block)
        #print("chain is ",self.chain)
    def remove(self,block):
        self.chain.remove(block)
        
    def mine(self,block):
        #print("in mining")
        
        try:
            
            block.previous_hash = self.chain[-1].hashing()
            
        except:
            pass
       
        while True:
            
            hash = hashing(block.previous_hash,block.number,block.data,block.nonce)

            
            if hash[:self.difficulty] == "0" * self.difficulty:
                
                block.hash = hash
                self.add(block)
                break;
            else:
                block.nonce += 1
    def isValid(self):
        
        for each in range(1,len(self.chain)):
            if self.chain[each].previous_hash != self.chain[each-1].hashing():
                return False
        return True

