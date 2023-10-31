#------------------------------------Functions for EC2s instances termination and Load balancer and target groups deletion ----------------------------------------------------

#Function to terminate EC2 instances when not needed
def terminate_instances(ec2_serviceresource,instances_ids):
    for id in instances_ids:
        ec2_serviceresource.Instance(id).terminate()
    return("Instances terminated")

#Function to delete LoadBalancer
def delete_load_balancer(elbv2_serviceclient, load_balancer_arn):
    
    elbv2_serviceclient.delete_load_balancer(
        LoadBalancerArn=load_balancer_arn
    )

    return("Load Balancer, rules and listeners associated deleted")

#Function to delete target groups when not needed
def delete_target_groups(elbv2_seviceclient,target_groups_arns):
    for arn in target_groups_arns:
        elbv2_seviceclient.delete_target_group(
        TargetGroupArn=arn
    )
    return("Target Groups deleted")
