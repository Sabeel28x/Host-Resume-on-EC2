# retrieve_instances.py

import boto3
import sys

def get_instance_ips(target_group_name):
    client = boto3.client('elbv2')

    # Retrieve Target Group ARN
    target_groups = client.describe_target_groups(Names=[target_group_name])
    if not target_groups['TargetGroups']:
        print("Target Group not found")
        sys.exit(1)

    target_group_arn = target_groups['TargetGroups'][0]['TargetGroupArn']

    # Retrieve Target Health
    target_health = client.describe_target_health(TargetGroupArn=target_group_arn)
    instance_ids = [desc['Target']['Id'] for desc in target_health['TargetHealthDescriptions']]

    if not instance_ids:
        print("No instances found")
        sys.exit(1)

    # Retrieve Public IPs of Instances
    ec2_client = boto3.client('ec2')
    instances = ec2_client.describe_instances(InstanceIds=instance_ids)
    instance_ips = [instance['PublicIpAddress'] for reservation in instances['Reservations'] for instance in reservation['Instances']]

    return instance_ips

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python retrieve_instances.py <target_group_name>")
        sys.exit(1)

    target_group_name = sys.argv[1]
    instance_ips = get_instance_ips(target_group_name)
    print("\n".join(instance_ips))
