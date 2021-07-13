import hashlib as hl
import datetime
import os
import struct
import json

from json import JSONEncoder, JSONDecoder

now = datetime.datetime.now
path = os.path.abspath(os.path.dirname(__file__))

class BlockEncoder(JSONEncoder): #Custom json encoder needed to encode the Block class
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return(o.__str__())

        return(o.__dict__)


class Block: #Block class
    def __init__(self, index, data, time, lh):
        self.index = index
        self.time = time
        self.data = data
        self.lh = lh
        self.hash = self.hashBlock()

    def hashBlock(self): #Calculates hash of block
        hasher = hl.sha256()
        hasher.update(f"""{self.index}
                       {self.time}
                       {self.data}
                       {self.lh}""".encode())

        return(hasher.hexdigest())


chain = []

def saveChain(): #Save chain to chain.json using custom encoder
    if os.access(path, os.W_OK):
        with open("chain.json", "w") as f:
            f.write(json.dumps(chain, cls=BlockEncoder))

def loadChain(): #Load chain from chain.json using custom decoder
    global chain

    def decode(obj):
        return(Block(obj["index"], obj["data"], obj["time"], obj["lh"]))

    if os.access(path+"/chain.json", os.R_OK):
        with open("chain.json", "r") as f:
            chain = JSONDecoder(object_hook = decode).decode(f.read())

def createBlock(data): #Creates a new block, adding it to the chain and saving the ledger
    global chain

    if len(chain) == 0:
        lh = 0
    else:
        lh = chain[-1].hash

    chain.append(Block(len(chain), data, now(), lh))
    saveChain()

loadChain()
if len(chain) == 0: #If chain is empty, create genesis block
    createBlock("Genesis block")
