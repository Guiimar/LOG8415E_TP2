# LOG8415E_TP2

This repository is for Lab assignment about Deploying Webapps executing ML models on Containers on AWS

Presented by :
- Mehdi Belchiti
- Anass EL AZOUZI
- Zakaria Haniri
- Guillaume MARTIN

Before running the codes, please make sure that :

- You have already installed Python 3 on his PC.
- You have already the last upgrade of pip.
- You have already installed Docker on his PC.
- You have an AWS account  in order to fill in the credential.ini file with your AWS credentials (aws_access_key_id,aws_secret_access_key,aws_session_token).

Then, you need to follow the steps below :

- First, please run Setup_main.py file : In this code you will create your 5 ec2 instances (4 workers and 1 Orchestrator), and install flask applications in each instance while creating it by passing dynamically into UserData argument of create_instance_ec2 function of boto3 the files below:

  -  For the Orchestrator: flask_orchestrator.sh file in which we create flask appl to receive POST requests from the user and orchestrate their forwarding to the workers.
  -  For the workers: flask_workers.sh file in which we create a docker file and compose two containers listening to different ports, and install a flask app to run ML models following received POST requests sent from the Orchestrator.

NB : Note that the file Setup_main.py use functions imported from Setup_functions.py file

- Second, please run Sending_request.py file : In this code you will retrieve dynamically the ip address of the Orchestrator you created before, and then you will send multiple POST requests in parallel to the Orchestrator and you will see all of the responses of ML applications already launched inside your workers containers (Input text and probabilities).
