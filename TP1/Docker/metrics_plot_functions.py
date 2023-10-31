import boto3 
import matplotlib.pyplot as plt

#Function to create Cloudwatch client:
def client_cloudwatch(aws_access_key_id, aws_secret_access_key, aws_session_token):
    cloudwatch_client =  boto3.client('cloudwatch',
                       'us-east-1',
                       aws_access_key_id= aws_access_key_id,
                       aws_secret_access_key=aws_secret_access_key ,
                       aws_session_token= aws_session_token) 
   
    return(cloudwatch_client)

#Function to get and plot Cloudwatch metrics per target groups of an ALB in a specific time interval: 
def plot_metric_clusters(Cloudwatch_client,Id,MetricName,LoadBalancerarn,TargetGroups_arns_list,Start_Time, End_Time,Period,Stat,path):
        plt.figure(figsize=(15,10))
        arn_lb=LoadBalancerarn.split('/')
        arn_lb=arn_lb[1]+'/'+arn_lb[2]+'/'+arn_lb[3]
        for TargterGroup in  TargetGroups_arns_list:
            arn_tg=TargterGroup.split(':')
            arn_tg=arn_tg[5]
            Target_cloudwatch=Cloudwatch_client.get_metric_data(
                MetricDataQueries=[
                    {
                        'Id':Id,
                        'MetricStat':{
                            'Metric':{
                                'Namespace': 'AWS/ApplicationELB',
                                'MetricName':MetricName,
                                'Dimensions':[
                                    {
                                        'Name':'LoadBalancer',
                                        'Value': arn_lb
                                            
                                    },
                                    {
                                        'Name':'TargetGroup',
                                        'Value':arn_tg

                                    }
                                ],

                            },
                        'Stat':Stat,
                        'Period':Period,

                        },
                        'ReturnData':True
                    },
                ],
                StartTime=Start_Time,
                EndTime=End_Time,
            )
            metric_list=Target_cloudwatch['MetricDataResults'][0]['Values']
            time_stamps=Target_cloudwatch['MetricDataResults'][0]['Timestamps']
            plt.plot(time_stamps,metric_list,label=arn_tg)
        plt.xlabel('Time')
        plt.ylabel(str(MetricName))
        plt.title(str(MetricName)+' per cluster')
        plt.legend(loc='upper right')
        plt.tight_layout()
        plt.savefig(path+str(MetricName)+'_per_cluster.png')


#Function to get and plot instances metrics per cluster and save it in a graph: 
def plot_Instances_metrics_per_cluster(Cloudwatch_client,Id,Cluster_name,MetricName,Instances_Ids,Start_Time, End_Time,Period,Stat,path):
        plt.figure(figsize=(15,10))
        for i in range(len(Instances_Ids)) :
            EC2_Id=Instances_Ids[i]
            EC2_Cloudwatch=Cloudwatch_client.get_metric_data(
                MetricDataQueries=[
                    {
                        'Id':Id,
                        'MetricStat':{
                            'Metric':{
                                'Namespace': 'AWS/EC2',
                                'MetricName':MetricName,
                                'Dimensions':[{'Name':'InstanceId',
                                        'Value': EC2_Id
                                            
                                    }
                                ]
                            },
                        'Stat':Stat,
                        'Period':Period,

                        },
                        'ReturnData':True,
                    },
                ],
                StartTime=Start_Time,
                EndTime=End_Time
                )
            metric=EC2_Cloudwatch['MetricDataResults'][0]['Values']
            timestimps=EC2_Cloudwatch['MetricDataResults'][0]['Timestamps']
            plt.plot(timestimps,metric,label=Cluster_name+' EC2_Id= '+EC2_Id)
        plt.xlabel('Time')
        plt.ylabel(str(MetricName)+' per instance')
        plt.title('EC2 Instances '+str(MetricName)+ ' of: '+Cluster_name)
        plt.legend(loc='upper right')
        plt.tight_layout()
        plt.savefig(path+'EC2_Instances_'+str(MetricName)+'_of_'+Cluster_name+'.png')

        
        
   

