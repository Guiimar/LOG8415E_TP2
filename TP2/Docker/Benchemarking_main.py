import configparser
import boto3
from datetime import datetime, timedelta
from Test_scenario_functions import *
from metrics_plot_functions import *
import os


if __name__ == '__main__':
    # Get credentials from the config file :
    #path = os.path.dirname(os.getcwd())

    config_object = configparser.ConfigParser()
    with open("credentials.ini","r") as file_object:
        config_object.read_file(file_object)
        key_id = config_object.get("resource","aws_access_key_id")
        access_key = config_object.get("resource","aws_secret_access_key")
        session_token = config_object.get("resource","aws_session_token")
        ami_id = config_object.get("ami","ami_id")

    
        
#============================>Benchemarking

    #------------------------------------------Get Setup data --------------------------------------------------------------------

    elbv2_client =  boto3.client('elbv2',
                       'us-east-1',
                       aws_access_key_id= key_id,
                       aws_secret_access_key=access_key ,
                      aws_session_token= session_token)
    
    #LoadBalancer Url DNS
    url = elbv2_client.describe_load_balancers()['LoadBalancers'][0]['DNSName']
    #LoadBalancer Arn
    load_balancerarn=elbv2_client.describe_load_balancers()['LoadBalancers'][0]['LoadBalancerArn']
    #Target Groups arns and names lists
    TargetGroups_arns_list=[tg['TargetGroupArn'] for tg in elbv2_client.describe_target_groups()['TargetGroups'] ]
    TargetGroups_names_list=[tg['TargetGroupName'] for tg in elbv2_client.describe_target_groups()['TargetGroups'] ]

    #Instances Ids of TG1
    Instances_Ids_TG1=[Instance['Target']['Id'] for Instance in elbv2_client.describe_target_health(TargetGroupArn=TargetGroups_arns_list[0])['TargetHealthDescriptions']]
    #Instances Ids of TG2
    Instances_Ids_TG2=[Instance['Target']['Id'] for Instance in elbv2_client.describe_target_health(TargetGroupArn=TargetGroups_arns_list[1])['TargetHealthDescriptions']]
    print('\nAll Setup data are retrieved successfully')    
    #------------------------------------------Sending requests -------------------------------------------------------------------
    time.sleep(120)
    print('\n=================================> Test Scenario Begins')
    # The start time of the test scenario
    StartTime=datetime.utcnow()
    print(StartTime)
    #Sending Two threads using the two paths (/Cluster1 and /Cluster2)
    for path in ['cluster1','cluster2']:
        print('\n'+str(datetime.utcnow())+'---Sending Threads to: '+str(path)+'---')
        #Defining the threads
        first_sending_thread=Thread(target=first_thread,args=(url,path))
        second_sending_thread=Thread(target=second_thread,args=(url,path))
        #Sending the threads
        first_sending_thread.start()
        second_sending_thread.start()
        
        first_sending_thread.join()
        second_sending_thread.join()
        print(str(datetime.utcnow())+'---Finishing for: '+str(path)+'---')

    # The start time of the test scenario
    EndTime=datetime.utcnow()
    print(EndTime)

    print('\n============================>Test Scenario ends')


    #---------------------------------------------Plot metrics ---------------------------------------------------------------------
    #Create Cloudwatch client
    print('\n============================>Ploting metrics...')

    time.sleep(120)
    Cloudwatch_client=client_cloudwatch(key_id, access_key, session_token)

    
    #Data retrieving period in secondes
    Period=60
    #Path to save the plots
    path='Metrics_test\\'


    #Plot 'RequestCount' metric per cluster in the specified path
    plot_metric_clusters(Cloudwatch_client,'metric1','RequestCount',load_balancerarn,TargetGroups_arns_list,StartTime-timedelta(minutes=2),EndTime+timedelta(minutes=2),Period,'Sum',path)

    
    #Plot 'TargetResponseTime' metric per cluster in the specified path
    plot_metric_clusters(Cloudwatch_client,'metric2','TargetResponseTime',load_balancerarn,TargetGroups_arns_list,StartTime-timedelta(minutes=2),EndTime+timedelta(minutes=2),Period,'Average',path)
    

    #Plot Average 'CPUUtilization' metric of all instances per cluster
    plot_Instances_metrics_per_cluster(Cloudwatch_client,'metric3',TargetGroups_names_list[0],'CPUUtilization',Instances_Ids_TG1,StartTime-timedelta(minutes=30), EndTime+timedelta(minutes=30),Period,'Average',path)
    plot_Instances_metrics_per_cluster(Cloudwatch_client,'metric4',TargetGroups_names_list[1],'CPUUtilization',Instances_Ids_TG2,StartTime-timedelta(minutes=30), EndTime+timedelta(minutes=30),Period,'Average',path)


    print('============================>Ploting metrics ends')


