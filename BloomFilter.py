from bitarray import bitarray
import mmh3
import numpy as np


class simpleBloomFilter:
    '''
    Class for Bloom filter, using murmur3 hash function
    '''
    def __init__(self, item_count, fp_prob):
        '''
        Inputs:
        item_count - expected number of items stored in the filter
        fp_prob - expected false positive probability in decimal
        '''
        self.item_count = item_count
        self.fp_prob = fp_prob
        self.hash_count = self.get_hash_count(self.fp_prob)
        self.size = self.get_size(self.item_count, self.fp_prob)
        self.bit_array = bitarray(self.size)
        self.bit_array.setall(0) 
       
    def add(self, string):
        '''
        Add and item in the filter
        '''
        for seed in range(self.hash_count):
            index = mmh3.hash(string, seed) % self.size
            self.bit_array[index] = 1
   
    
    def lookup(self, string):
        '''
        Look up if an item is in the filter
        '''
        for seed in range(self.hash_count):
            index = mmh3.hash(string, seed) % self.size
            if self.bit_array[index] == 0:
                return False
        return True
    
    
    @classmethod
    def get_size(self, n, p):
        '''
        Return the size of the filter.
        n: expected number of items in the filter
        p: False Positive probability in decimal
        '''
        m = -(n*np.log(p))/(np.log(2))**2
        return int(m)

    @classmethod
    def get_hash_count(self, p):
        '''
        Return the number of hash functions used.
        p: False Positive probability in decimal
        '''
        k = - np.log2(p)
        return int(k)
    
    
    



