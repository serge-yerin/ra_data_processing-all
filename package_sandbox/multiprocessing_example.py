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
