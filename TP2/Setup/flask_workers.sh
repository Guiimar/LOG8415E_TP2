# Add Docker's official GPG key:
sudo apt-get -y update
sudo apt-get -y install ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Add the repository to Apt sources:
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get -y update

#To install the latest version
sudo apt-get -y install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

#create a directory for the compose:
mkdir /home/ubuntu/composeflask && cd /home/ubuntu/composeflask

#create and write the flask app script:
cat <<EOL > /home/ubuntu/composeflask/flask_app.py
from flask import Flask,jsonify
from transformers import DistilBertTokenizer,DistilBertForSequenceClassification
import torch
import random
import string

app=Flask(__name__)

tokenizer=DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
model=DistilBertForSequenceClassification.from_pretrained('distilbert-base-uncased',num_labels=2)

def generate_random_text(length=50):
    letters=string.ascii_lowercase + ' '
    return ''.join(random.choice(letters) for i in range(length))

@app.route('/run_model',methods=['POST'])
def run_model():
    input_text=generate_random_text()
    inputs=tokenizer(input_text,return_tensors='pt',padding=True,truncation=True)
    outputs=model(**inputs)

    probabilities=torch.softmax(outputs.logits,dim=-1)

    probabilities_list=probabilities.tolist()[0]

    return jsonify({"input_text": input_text,"probabilities":probabilities_list})

if __name__=='__main__':
    # TO BE ADJUST FOR ADEQUATE 
    app.run(host='0.0.0.0',port=5000)

EOL

#create requirements file:
cat <<EOL > /home/ubuntu/composeflask/requirements.txt
flask
transformers
torch
EOL

#create a dockerfile:
cat <<EOL > /home/ubuntu/composeflask/Dockerfile
# syntax=docker/dockerfile:1
FROM python:3.8
RUN pip install --upgrade pip
WORKDIR /code
ENV FLASK_APP=flask_app.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["flask", "run"]
EOL

#first container on 5000:
cat <<EOL > /home/ubuntu/composeflask/compose.yaml
services:
  webapp1:
    build: .
    ports:
      - "5000"
  webapp2:
    build: .
    ports:
      - "5001:5000"
EOL

docker compose up -d
