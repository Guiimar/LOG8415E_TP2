import requests
import time
from threading import Thread
from datetime import datetime



def consumeGETRequestSync(url_lb,path):
    try:
        url="http://{}/{}".format(url_lb, path)
        r=requests.get(url)
    except Exception as e:
        print('Exception returned is',e)

def first_thread(lb_dns,path):
    print(str(datetime.utcnow())+' :Starting sending 1000 requests of Thread 1')
    for _ in range(1000):
        consumeGETRequestSync(lb_dns,path)
    print(str(datetime.utcnow())+' :Finishing sending 1000 requests of Thread 1')

    #5OO requests then 60 seconds sleep then 1000 requests
def second_thread(lb_dns,path):
    print(str(datetime.utcnow())+' :Starting sending 500 requests of Thread 2')
    for _ in range(500):
        consumeGETRequestSync(lb_dns,path)
    print(str(datetime.utcnow())+' :Finishing sending 500 requests of Thread 2')
    print('Waiting for 60 secondes') 
    time.sleep(60)
    print(str(datetime.utcnow())+' :Starting sending 1000 requests of Thread 2')
    for _ in range(1000):
        consumeGETRequestSync(lb_dns,path)
    print(str(datetime.utcnow())+' :Finishing sending 1000 + 500 requests of Thread 2')

