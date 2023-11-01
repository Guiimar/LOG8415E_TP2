import configparser
import boto3
import time

#Function to create a service resource for ec2: 
def resource_ec2(aws_access_key_id, aws_secret_access_key, aws_session_token):
    ec2_serviceresource =  boto3.resource('ec2',
                       'us-east-1',
                       aws_access_key_id= aws_access_key_id,
                       aws_secret_access_key=aws_secret_access_key ,
                      aws_session_token= aws_session_token) 
    
    return(ec2_serviceresource)

#Function to create a service client for ec2
def client_ec2(aws_access_key_id, aws_secret_access_key, aws_session_token):
    ec2_serviceclient =  boto3.client('ec2',
                       'us-east-1',
                       aws_access_key_id= aws_access_key_id,
                       aws_secret_access_key=aws_secret_access_key ,
                      aws_session_token= aws_session_token) 
   
    
    return(ec2_serviceclient)

#Function to create and check a KeyPair : 
def create_keypair(key_pair_name, client):
    try:
        keypair = client.create_key_pair(KeyName=key_pair_name)
        print(keypair['KeyMaterial'])
        with open('lab1_keypair.pem', 'w') as f:
            f.write(keypair['KeyMaterial'])

        return(key_pair_name)

    except:
        print("\n\n============> Warning :  Keypair already created !!!!!!!<==================\n\n")
        return(key_pair_name)


#---------------------------------------------To re check----------------------------------------------
'Function to create a new vpc (Maybe no need for this, just use default vpc)'
def create_vpc(CidrBlock,resource):
   VPC_Id=resource.create_vpc(CidrBlock=CidrBlock).id
   return VPC_Id

'Function to create security group (Maybe no need for this, just use get securty group of default vpc)'
def create_security_group(Description,Groupe_name,vpc_id,resource):
    Security_group_ID=resource.create_security_group(
        Description=Description,
        GroupName=Groupe_name,
        VpcId=vpc_id).id
    
    Security_group=resource.SecurityGroup(Security_group_ID)
    
    #Add an inbounded allowing inbounded traffics of all protocols, from and to all ports, and all Ipranges.  
    Security_group.authorize_ingress(
         IpPermissions=[
            {'FromPort':-1,
             'ToPort':-1,
             'IpProtocol':'-1',
             'IpRanges':[{'CidrIp':'0.0.0.0/0'}]
            }]
    )       
    return Security_group_ID

#------------------------------------------------End----------------------------------------------------


#Function to create ec2 instances : 
def create_instance_ec2(num_instances,ami_id,
    instance_type,key_pair_name,ec2_serviceresource,security_group_id,Availabilityzons, user_data):
    instances=[]
    for i in range(num_instances):
        instance=ec2_serviceresource.create_instances(
            ImageId=ami_id,
            InstanceType=instance_type,
            KeyName=key_pair_name,
            MinCount=1,
            MaxCount=1,
            Placement={'AvailabilityZone':Availabilityzons[i]},
            SecurityGroupIds=[security_group_id] if security_group_id else [],
            UserData=user_data,
            TagSpecifications=[
                    {
                        'ResourceType': 'instance',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'lab1-ec2-instance-'+str(instance_type)+"-"+str(i + 1)
                            },
                        ]
                    },
                ]
        )
        instances.append(instance[0].id)
        print ('Instance: ',i+1,' having the Id: ',instance[0].id, ' in Availability Zone: ', Availabilityzons[i], 'is created')
        #print(f'{instances[i]} is starting')
   
    return instances
