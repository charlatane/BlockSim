import numpy as np
from InputsConfig import InputsConfig as p
from Models.Bitcoin.Node import Node
from Models.Consensus import Consensus as BaseConsensus
from Models.Bitcoin.ChainConsensus import group_chain_complexity as gcc
import random
import math

class Consensus(BaseConsensus):

    """
	We modelled PoW consensus protocol by drawing the time it takes the miner to finish the PoW from an exponential distribution
        based on the invested hash power (computing power) fraction
    """
    def Protocol(miner):
        ##### Start solving a fresh PoW on top of last block appended #####
        ##GROUPCHAIN###
        TOTAL_HASHPOWER = sum([miner.hashPower for miner in p.NODES])
        hashPower = miner.hashPower/TOTAL_HASHPOWER
        groupComplexity = gcc()
        pow_generator = (random.expovariate(hashPower*(1/p.Binterval)))
        print((pow_generator+groupComplexity)/random.randint(8, 12))
        return ((pow_generator+groupComplexity)/random.randint(8, 12))
        ##GROUPCHAIN ENDS###


        # n=1000;
        # m=30;
        # logn=math.log(n, 10)
        # logm=math.log(m, 10)

        # print((((n*logn)/random.randint(20,30))+2*m*logm)*(0.3))
        # return ((((n*logn)/random.randint(20,30))+2*m*logm)*(0.3))




    """
	This method apply the longest-chain approach to resolve the forks that occur when nodes have multiple differeing copies of the blockchain ledger
    """
    def fork_resolution():
        BaseConsensus.global_chain = [] # reset the global chain before filling it

        a=[]
        for i in p.NODES:
            a+=[i.blockchain_length()]
        x = max(a)

        b=[]
        z=0
        for i in p.NODES:
            if i.blockchain_length() == x:
                b+=[i.id]
                z=i.id

        if len(b) > 1:
            c=[]
            for i in p.NODES:
                if i.blockchain_length() == x:
                    c+=[i.last_block().miner]
            z = np.bincount(c)
            z= np.argmax(z)

        for i in p.NODES:
            if i.blockchain_length() == x and i.last_block().miner == z:
                for bc in range(len(i.blockchain)):
                    BaseConsensus.global_chain.append(i.blockchain[bc])
                break
