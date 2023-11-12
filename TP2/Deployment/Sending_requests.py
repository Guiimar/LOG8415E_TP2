import boto3
import requests
import multiprocessing
import configparser
import os
from datetime import date
import time

#Function to send a POST request (to orchestrator)
# The info list contains the ip, the port of the orchestrator and then the data to send in the request 
def send_request_to_orchestrator(info):
    ip=info[0]
    port=info[1]
    data=info[2]
    try:
        url="http://{}:{}/{}".format(ip, port,'new_request')
        # Sending the request
        response=requests.post(url,data=data)
        ls = response.json()
        print(ls)
    except Exception as e:
        print('Exception returned is',e)

#Function to send a get request just to get the full json file of responses received from containers
def send_request_results(ip,port):
    try:
        url="http://{}:{}/{}".format(ip, port,'get_results')
        # Sending the send request
        response=requests.get(url)
        print(response.text)
    except Exception as e:
        print('Exception returned is',e)

#Function to send multiple POST request to orchestrator in parallel using multiprocessing library of python
def send_multiple_requests(info,num_requests):
    # Create a pool to send multiple requests to the orchestrator in parallel
    pool = multiprocessing.Pool(processes=num_requests)
    # Mapping requests to send them in parallel to orchestrator simultaneously
    pool.map(send_request_to_orchestrator, [info]*num_requests)

    # It's to desable any other incoming request 
    pool.close()
    # It's to block running the code until all requests are executed 
    pool.join()
   

if __name__ == '__main__':
    # Get credentials from the config file :
    path = os.path.dirname(os.getcwd())
    path=path+"\TP2"
    config_object = configparser.ConfigParser()
    with open(path+"/credentials.ini","r") as file_object:
        config_object.read_file(file_object)
        key_id = config_object.get("resource","aws_access_key_id")
        access_key = config_object.get("resource","aws_secret_access_key")
        session_token = config_object.get("resource","aws_session_token")

    # Create an ec2 client 
    ec2_serviceclient = boto3.client('ec2',
                        'us-east-1',
                        aws_access_key_id= key_id,
                        aws_secret_access_key=access_key ,
                        aws_session_token= session_token) 
    
    # Get description of the Orchestrator data 
    response_orch = ec2_serviceclient.describe_instances(Filters=[{'Name': 'tag:Name', 'Values': ['lab2-orchestrator-1']}])
    #Get the ip address of the  Orchestrator
    ip_address_orchestrator=response_orch["Reservations"][0]["Instances"][0]["PublicIpAddress"]
    #ip_address_orchestrator = ""
    #print(ip_address_orchestrator)


    #Definate orchestrator port, data to send to it, and number of requests 
    orchestrator_port=80
    data='Hello'
    num_requests=5

    #Send requests to orchestrator 
    info=[ip_address_orchestrator,orchestrator_port,data]
    print('Starting sending requests to orchestrator simultaneously') 
    send_multiple_requests(info,num_requests)
    print('Finished sending requests')
    #send_request_results(ip_address_orchestrator,orchestrator_port)
    




