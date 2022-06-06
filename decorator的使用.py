# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 14:33:07 2022

@author: xfugm
"""
import time

def display_time(func):
    def wrapper(*args):
        t1 = time.time()
        x = func(*args)
        t2 = time.time()
        print(t2-t1)
        return x
    return wrapper


def is_prime(num):
    if num<2:
        return False
    elif num == 2:
        return True
    else:
        for i in range(2,num):
            if num % i == 0:
                return False
            return True
        
@display_time
def count_prime_nums(num):
    count = 0
    for i in range(2,num):
        if is_prime(i):
            count = count+1
    return count

count = count_prime_nums(10000)
print(count)
