import pulumi_aws as aws
from instance.security_groups import allow_443_outbound_to_private_subnet_cidr
from network.vpc import data_vpc
from network.config import ENV

allow_443_inbound_from_private_instance_sg = aws.ec2.SecurityGroup(
    "allow_443_inbound_from_private_instance_sg",
    description="Allow inbound traffic from instance SG in private subnet",
    vpc_id=data_vpc.id,
    tags={"Name": f"{ENV}-allow-443-inbound-from-private-instance-sg", "env": ENV},
)

aws.vpc.SecurityGroupIngressRule(
    "allow_443_inbound_from_private_instance_sg_ingress_rule",
    security_group_id=allow_443_inbound_from_private_instance_sg.id,
    ip_protocol="tcp",
    referenced_security_group_id=allow_443_outbound_to_private_subnet_cidr.id,
    from_port=443,
    to_port=443,
)
