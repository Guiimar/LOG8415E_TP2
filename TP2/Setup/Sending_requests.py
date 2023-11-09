import boto3
import requests
import multiprocessing
import configparser
import os
from datetime import date

#Function to send request (to orchestrator)
def send_request_to_orchestrator(info):
<<<<<<< HEAD
    ip=info[0]
    port=info[1]
    data=info[2]
=======
    ip=info[0],port=info[1],data=info[2]
>>>>>>> 38f1a6b2b80d744be4d5424fa09de4df0abf0022
    try:
        url="http://{}:{}/{}".format(ip, port,'new_request')
        #post pour transmettre la requête
        response=requests.post(url,data=data)
    except Exception as e:
        print('Exception returned is',e)

def send_multiple_requests(info,num_requests):
    # Create a pool to distribute tasks among multiple processes :
    print('Ok')
    pool = multiprocessing.Pool(processes=num_requests)
<<<<<<< HEAD
    print('Ok')
=======
 
>>>>>>> 38f1a6b2b80d744be4d5424fa09de4df0abf0022
    # use a pool of worker processes to send multiple HTTP requests simultaneously :
    pool.map(send_request_to_orchestrator, [info]*num_requests)
    print('Ok')
    # Desable any other incoming request
    pool.close()
    # block running until all requests are executed 
    pool.join()
   

if __name__ == '__main__':
    # Get credentials from the config file :
    path = os.path.dirname(os.getcwd())
    #path=path+"\TP2"
    config_object = configparser.ConfigParser()
    with open(path+"\credentials.ini","r") as file_object:
        config_object.read_file(file_object)
        key_id = config_object.get("resource","aws_access_key_id")
        access_key = config_object.get("resource","aws_secret_access_key")
        session_token = config_object.get("resource","aws_session_token")

    # Get ip address of Orchestrator
    ec2_serviceclient = boto3.client('ec2',
                        'us-east-1',
                        aws_access_key_id= key_id,
                        aws_secret_access_key=access_key ,
                        aws_session_token= session_token) 
    
        
    response = ec2_serviceclient.describe_instances(Filters=[{'Name': 'tag:Name', 'Values': ['lab2-orchestrator-1']}])
    ip_address_orchestrator=response['Reservations'][0]['Instances'][0]['PublicIpAddress']
<<<<<<< HEAD
    print(ip_address_orchestrator)
=======
   

>>>>>>> 38f1a6b2b80d744be4d5424fa09de4df0abf0022
    # Send requests to orchestrator
    orchestrator_port=5000
    data='Hello'
    num_requests=5

<<<<<<< HEAD
    info=[ip_address_orchestrator,orchestrator_port,data]
=======
    # print (date.utcnow())
>>>>>>> 38f1a6b2b80d744be4d5424fa09de4df0abf0022
    print('Starting sending requests to orchestrator simultaneously') 
    send_multiple_requests(info,num_requests)
    print('Finished sending requests') 
<<<<<<< HEAD
    
=======
    #print (date.utcnow())
>>>>>>> 38f1a6b2b80d744be4d5424fa09de4df0abf0022




