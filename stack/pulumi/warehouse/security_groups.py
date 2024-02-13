import pulumi_aws as aws
from warehouse.config import ENV
from network.vpc import data_vpc
from network.private_subnets import private_subnet

allow_5432_inbound_from_private_subnet = aws.ec2.SecurityGroup(
    "data_warehouse_sg",
    description="Allow inbound traffic only if it is coming from instance inside the private subnet",
    vpc_id=data_vpc.id,
    tags={"Name": f"{ENV}-data-warehouse-sg", "env": ENV},
)

allow_5432_inbound_from_private_subnet_ingress_rule = aws.vpc.SecurityGroupIngressRule(
    "data_warehouse_sg_ingress_rule",
    security_group_id=allow_5432_inbound_from_private_subnet.id,
    from_port=5432,
    to_port=5432,
    ip_protocol="tcp",
    cidr_ipv4=private_subnet.cidr_block,
)
