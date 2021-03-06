#!/usr/bin/python

# Import troposphere
from troposphere import Template, Ref, Output, Join, GetAtt, Parameter
import troposphere.ec2 as ec2
from troposphere.ec2 import Subnet

# Create a template for resources to live in
template = Template()

keypair = template.add_parameter(
    Parameter(
        'KeyName',
        ConstraintDescription='must be the name of an existing EC2 KeyPair.',
        Description='Name of an existing EC2 KeyPair to enable SSH access to \
the instance',
        Type='AWS::EC2::KeyPair::KeyName',
    ))

subnet = template.add_parameter(Parameter(
    'Subnets',
    Type = 'AWS::EC2::Subnet::Id',
    Description=(
        "The list of SubnetIds, for at least two Availability Zones in the "
        "region in your Virtual Private Cloud (VPC)")
))

# trying to get User Data working
UserData=Base64(Join('', [
    '#!/bin/bash\n',
    'yum update'

    ]
    )
)

# Create an instance
instance = ec2.Instance("MyInstance")
instance.ImageId = "ami-ebadaedb"
instance.InstanceType = "t2.micro"
instance.KeyName = Ref(keypair)
instance.SubnetId = Ref(subnet)


template.add_resource(instance)

# Add output to template
template.add_output(Output(
    "InstanceAccess",
    Description="Command to use to SSH to instance",
    Value=Join("", ["ssh -i ", Ref(keypair), " ubuntu@", GetAtt(instance, "PublicDnsName")])
))

# Print out CloudFormation template in JSON
print template.to_json()