import os
import configparser

config_object = configparser.ConfigParser()

path = os.path.dirname(os.getcwd())


# Change the current working directory to the parent directory

with open(path+"/credentials.ini","r") as file_object:
    config_object.read_file(file_object)
key_id = config_object.get("resource","aws_access_key_id")
access_key = config_object.get("resource","aws_secret_access_key")
session_token = config_object.get("resource","aws_session_token")
ami_id = config_object.get("ami","ami_id")

print(key_id)