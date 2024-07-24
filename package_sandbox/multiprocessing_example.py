"""
from multiprocessing import Process
import time


def f1():
    print('F1 starts ')
    time.sleep(10)
    p2 = Process(target=f2, args=())
    p2.start()
    time.sleep(10)
    print('F1 ends')
    p2.join()

def f2():
    print('F2 starts')
    time.sleep(4)
    print('F2 continues')
    time.sleep(4)
    print('F2 stops')

if __name__ == '__main__':

    p1 = Process(target=f1, args=())
    p1.start()
    p1.join()

"""

import multiprocessing 

def square(x, *args, **kwargs) : # , **kwargs
    
    print("\n",  x, args[0], kwargs, "\n")
    
    return kwargs["n"] 
  
if __name__ == '__main__': 
    n_proc = 3
    pool = multiprocessing.Pool() 
    my_kwargs_1 = {'n': 3}
    my_kwargs_2 = {'a': 5}
    args = ("a", )
    
    result_async = [pool.apply_async(square, (1, ) + args , {**{"c": i}, **my_kwargs_1}) for i in range(10)] 
    
    results = [r.get() for r in result_async] 

    print("Output: {}".format(results)) 
    
    
    
# import multiprocessing 

# def square(x): 
#     return x * x 

# if __name__ == '__main__': 
#     pool = multiprocessing.Pool() 
#     result_async = [pool.apply_async(square, args = (i, )) for i in range(10)] 
#     results = [r.get() for r in result_async]
#     print("Output: {}".format(results))