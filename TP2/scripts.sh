#!/bin/bash
# Clone the git repository for the assignement 
git clone https://github.com/Guiimar/LOG8415E_TP2.git
# Open folder TP2
cd LOG8415/TP2
# Enter your AWS credentials here
new_aws_access_key="key"
new_aws_secret_key="secret"
new_aws_token_key="token"

# Fill in the credentials.ini file with entered aws_access_key
sed -i "s#aws_access_key_id=.*#aws_access_key_id=${new_aws_access_key}#" credentials.ini

# Fill in the credentials.ini file with entered new_aws_secret_key
sed -i "s#aws_secret_access_key=.*#aws_secret_access_key=${new_aws_secret_key}#" credentials.ini

# Fill in the credentials.ini file with entered new_aws_token_key
sed -i "s#aws_session_token=.*#aws_session_token=${new_aws_token_key}#" credentials.ini

# Install boto3
pip install boto3

#Execute Setup python file

'' In this code you will create your 5 ec2 instances (4 workers and 1 Orchestrator), and install flask applications in each instance.

While creating the orchestrator instance, we pass dynamically into UserData argument of create_instance_ec2 function of boto3 the file (flask_orchestrator.sh) in which we create flask appl to receive POST requests from the user and orchestrate their forwarding to the workers.

While creating the workers instances , we pass dynamically into UserData argument of create_instance_ec2 function of boto3 the file (flask_workers.sh) in which we create a docker file and compose two containers listening to different ports, and install a flask app to run ML models following received POST requests sent from the Orchestrator. ''

cd Deployement
python3 Setup_main.py

#Execute Sending request python file

'' In this code you will retrieve dynamically the ip address of the Orchestrator you created before, and then you will send multiple POST requests in parallel to the Orchestrator and you will see all of the responses of ML applications already launched inside your workers containers (Input text and probabilities). ''

cd Deployement
python3 Sending_request.py


