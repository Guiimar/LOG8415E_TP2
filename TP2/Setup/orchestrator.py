from flask import Flask,request,jsonify
import threading
import json
import time
import requests

app=Flask(__name__)
lock=threading.Lock()
request_queue=[]

def send_request_to_container(container_id,container_info,incoming_request_data):
    print(f"Sending request to {container_id} with data : {incoming_request_data}...")

    container_ip=container_info["ip"]
    container_port=container_info["port"]

    try:
        url="http://{}:{}/{}".format(container_ip, container_port,'run_model')
        #post pour transmettre la requête
        response=requests.post(url,data=incoming_request_data)
    except Exception as e:
        print('Exception returned is',e)

    #Code pour voir la réponse   
    if response.status_code == 200:
        data = response.json()
        input_text = data['input_text']
        probabilities = data['probabilities']
        print("Input Text:", input_text)
        print("Probabilities:", probabilities)
    else:
        print("La requête a échoué. Code d'état du serveur :", response.status_code)

    print(f"Received response from {container_id}")



def update_container_status(container_id,status):
    with lock:
        with open("test.json","r") as f:
            data=json.load(f)
        data[container_id]["status"]=status
        with open ("test.json","w") as f:
            json.dump(data,f)

def process_request(incoming_request_data):
    with lock:
        with open("test.json","r") as f:
            data=json.load(f)
    free_container=None
    for container_id, container_info in data.items():
        if container_info["status"]=="free":
            free_container=container_id
            break
    if free_container:
        update_container_status(free_container,"busy")
        send_request_to_container(
            free_container,data[free_container],incoming_request_data
        )
        update_container_status(free_container,"free")
    else:
        #### Les requetes sont dans la queue QUE FAIRE POUR LES TRAITER
        request_queue.append(incoming_request_data)    

# @app.route("/new_request",methods=["POST"])
# def new_request():
#     incoming_request_data=""
#     # Si les requetes sont dans la queue, mettre une gestion FIFO des ancieenes & nouvelles requetes
#     while request_queue:
#         threading.Thread(target=process_request,args=(request_queue,)).start()
#     threading.Thread(target=process_request,args=(incoming_request_data,)).start()

#     return jsonify({"message":"Request received and processing started."})

if __name__ == '__main__':

    incoming_request_data=""
    # Si les requetes sont dans la queue, mettre une gestion FIFO des ancieenes & nouvelles requetes
    while request_queue:
        threading.Thread(target=process_request,args=(request_queue,)).start()
    threading.Thread(target=process_request,args=(incoming_request_data,)).start()

    #return jsonify({"message":"Request received and processing started."})

