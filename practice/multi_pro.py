from multiprocessing import Process,Queue
import os,time,random

def write(q):
    print('Process to write: {}'.format(os.getpid()))
    for value in ['A','B','C']:
        print('Put {} to queue...'.format(value))
        q.put(value)
        time.sleep(random.random())

def read(q):
    print('Process to read: {}'.format(os.getpid()))
    while True:
        value = q.get(True)
        print('Get {} from queue.'.format(value))


if __name__ == '__main__':
    q = Queue()
    pw = Process(target=write,args=(q,))
    pr = Process(target=read,args=(q,))
    pw.start()
    pr.start()
    pw.join()
    pr.terminate()
