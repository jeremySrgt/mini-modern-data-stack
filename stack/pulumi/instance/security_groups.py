import pulumi_aws as aws
from network.vpc import data_vpc
from network.private_subnets import private_subnet
from instance.config import ENV


allow_443_outbound_to_private_subnet_cidr = aws.ec2.SecurityGroup(
    "allow_443_outbound_to_private_subnet_cidr",
    description="Allow 443 tcp outbound traffic to private subnet cidr",
    vpc_id=data_vpc.id,
    tags={"Name": f"{ENV}-allow-443-outbound-to-private-subnet-cidr", "env": ENV},
)

aws.vpc.SecurityGroupEgressRule(
    "allow_443_outbound_to_private_subnet_cidr_egress_rule",
    security_group_id=allow_443_outbound_to_private_subnet_cidr.id,
    ip_protocol="tcp",
    cidr_ipv4=private_subnet.cidr_block,
    from_port=443,
    to_port=443,
)


allow_outbound_to_anywhere = aws.ec2.SecurityGroup(
    "alllow_outbound_to_anywhere",
    description="Allow outbound traffic to anywhere, with the route table, this will go through NAT gw",
    vpc_id=data_vpc.id,
    tags={"Name": f"{ENV}-alllow-outbound-to-anywhere", "env": ENV},
)

aws.vpc.SecurityGroupEgressRule(
    "alllow_outbound_to_anywhere_egress_rule",
    security_group_id=allow_outbound_to_anywhere.id,
    ip_protocol="-1",
    cidr_ipv4="0.0.0.0/0",
)
