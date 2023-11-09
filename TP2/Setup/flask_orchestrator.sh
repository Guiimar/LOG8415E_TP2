#!/bin/bash

#Install Python Virtualenv

sudo apt-get -y update
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y python3-venv 

#Create directory

# if [ -d "flaskapp" ]; then
#   sudo rm -rf flaskapp
# fi 

mkdir /home/ubuntu/flaskapp && cd /home/ubuntu/flaskapp 

#Create the virtual environment

python3 -m venv venv

#Activate the virtual environment

source venv/bin/activate

#Install Flask
# pip install --upgrade pip
pip install Flask
pip install jsons
pip install flask-restful
pip install requests
pip install ec2_metadata

#Create json file that will cointain the IP addresses and port of cointainers:
cat <<EOL > /home/ubuntu/flaskapp/test.json
{"container1": {"ip": "52.201.230.99", "port": "5000", "status": "free"}, "container2": {"ip": "52.201.230.99", "port": "5001", "status": "free"}, "container3": {"ip": "54.161.72.199", "port": "5000", "status": "free"}, "container4": {"ip": "54.161.72.199", "port": "5001", "status": "free"}, "container5": {"ip": "54.227.48.172", "port": "5000", "status": "free"}, "container6": {"ip": "54.227.48.172", "port": "5001", "status": "free"}, "container7": {"ip": "3.90.137.20", "port": "5000", "status": "free"}, "container8": {"ip": "3.90.137.20", "port": "5001", "status": "free"}}
EOL

#Create of a simple Flask app:

cat <<EOL > /home/ubuntu/flaskapp/orchestrator.py
from flask import Flask,request,jsonify
import threading
import json
import time
import requests

app=Flask(__name__)
lock=threading.Lock()
request_queue=[]
path = "/home/ubuntu/flaskapp/"
#path = ""

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
        with open(path+"test.json","r") as f:
            data=json.load(f)
        data[container_id]["status"]=status
        with open (path+"test.json","w") as f:
            json.dump(data,f)

def process_request(incoming_request_data):
    with lock:
        with open(path+"test.json","r") as f:
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
        time.sleep(2)
        update_container_status(free_container,"free")
    else:
        #### Les requetes sont dans la queue QUE FAIRE POUR LES TRAITER
        request_queue.append(incoming_request_data)    

@app.route("/new_request",methods=["POST"])
def new_request():
    incoming_request_data=""
    # Si les requetes sont dans la queue, mettre une gestion FIFO des ancieenes & nouvelles requetes
    while request_queue:
        threading.Thread(target=process_request,args=(request_queue,)).start()
    threading.Thread(target=process_request,args=(incoming_request_data,)).start()

    return jsonify({"message":"Request received and processing started."})

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
    print('\n-----End-----')
    print('\n-----Please send other requests-----')

EOL

python /home/ubuntu/flaskapp/orchestrator.py

# #Install Gunicorn:

# pip install gunicorn

# #Create a file system containing service instructions:

# sudo cat <<EOL > /etc/systemd/system/flaskapp.service
# [Unit]
# Description=None
# After=network.target

# [Service]
# User=ubuntu
# Group=www-data
# WorkingDirectory=/home/ubuntu/flaskapp
# ExecStart=/home/ubuntu/flaskapp/venv/bin/gunicorn -b localhost:8000 orchestrator:app
# Restart=always

# [Install]
# WantedBy=multi-user.target
# EOL

# #Enable the service:

# sudo systemctl daemon-reload
# sudo systemctl start flaskapp
# sudo systemctl enable flaskapp

# #Check the app is running using:

# curl localhost:8000

# #Install nginx:

# sudo DEBIAN_FRONTEND=noninteractive apt-get -y install nginx

# #Start the Nginx service :

# sudo systemctl start nginx
# sudo systemctl enable nginx

# #Edition of /etc/nginx/sites-available/default in order to add  :

# sudo cat <<EOL > /etc/nginx/sites-available/default

# ##
# # You should look at the following URL's in order to grasp a solid understanding
# # of Nginx configuration files in order to fully unleash the power of Nginx.
# # https://www.nginx.com/resources/wiki/start/
# # https://www.nginx.com/resources/wiki/start/topics/tutorials/config_pitfalls/
# # https://wiki.debian.org/Nginx/DirectoryStructure
# #
# # In most cases, administrators will remove this file from sites-enabled/ and
# # leave it as reference inside of sites-available where it will continue to be
# # updated by the nginx packaging team.
# #
# # This file will automatically load configuration files provided by other
# # applications, such as Drupal or Wordpress. These applications will be made
# # available underneath a path with that package name, such as /drupal8.
# #
# # Please see /usr/share/doc/nginx-doc/examples/ for more detailed examples.
# ##

# # Default server configuration
# #
# upstream flaskhrunninginstance {
#     server 127.0.0.1:8000;
# }
# server {
#         listen 80 default_server;
#         listen [::]:80 default_server;

#         # SSL configuration
#         #
#         # listen 443 ssl default_server;
#         # listen [::]:443 ssl default_server;
#         #
#         # Note: You should disable gzip for SSL traffic.
#         # See: https://bugs.debian.org/773332
#         #
#         # Read up on ssl_ciphers to ensure a secure configuration.
#         # See: https://bugs.debian.org/765782
#         #
#         # Self signed certs generated by the ssl-cert package
#         # Don't use them in a production server!
#         #
#         # include snippets/snakeoil.conf;

#         root /var/www/html;

#         # Add index.php to the list if you are using PHP
#         index index.html index.htm index.nginx-debian.html;

#         server_name _;

#         location / {
#                 # First attempt to serve request as file, then
#                 proxy_pass http://flaskhrunninginstance ;
#                 # as directory, then fall back to displaying a 404.
#                 try_files $uri $uri/ =404;
#         }

#         # pass PHP scripts to FastCGI server
#         #
#         #location ~ \.php$ {
#         #       include snippets/fastcgi-php.conf;
#         #
#         #       # With php-fpm (or other unix sockets):
#         #       fastcgi_pass unix:/run/php/php7.4-fpm.sock;
#         #       # With php-cgi (or other tcp sockets):
#         #       fastcgi_pass 127.0.0.1:9000;
#         #}

#         # deny access to .htaccess files, if Apache's document root
#         # concurs with nginx's one
#         #
#         #location ~ /\.ht {
#         #       deny all;
#         #}
# }


# # Virtual Host configuration for example.com
# #
# # You can move that to a different file under sites-available/ and symlink that
# # to sites-enabled/ to enable it.
# #
# #server {
# #       listen 80;
# #       listen [::]:80;
# #
# #       server_name example.com;
# #
# #       root /var/www/example.com;
# #       index index.html;
# #
# #       location / {
# #               try_files $uri $uri/ =404;
# #       }
# #}
# EOL

# #Restart nginx:

# sudo systemctl restart nginx
