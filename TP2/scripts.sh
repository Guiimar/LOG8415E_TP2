#!/bin/bash
# Clone the git repository for the assignement 
git clone https://github.com/Guiimar/LOG8415.git
# Open folder TP1
cd LOG8415/TP1
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

# Copy credentials.ini file in Docker folder
cp credentials.ini Docker/

# Install boto3
pip install boto3

#Execute Setup python file
cd Setup
python3 Setup_main.py

# Open the folder Docker
cd ..
cd Docker

# Build Docker container
docker build -t test .
# Run container (containing Benchemark python file)
docker run -it test
