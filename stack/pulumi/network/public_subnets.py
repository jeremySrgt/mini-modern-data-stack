import pulumi_aws as aws
from network.vpc import data_vpc, internet_gateway
from network.config import ENV

public_subnet = aws.ec2.Subnet(
    "public_subnet",
    vpc_id=data_vpc.id,
    availability_zone="eu-west-3a",
    cidr_block="10.0.1.0/24",
    map_public_ip_on_launch=True,
    tags={"Name": f"{ENV}-data-public-subnet", "env": ENV},
)

public_subnet_route_table = aws.ec2.RouteTable(
    "public_subnet_route_table",
    vpc_id=data_vpc.id,
    routes=[
        aws.ec2.RouteTableRouteArgs(
            cidr_block="0.0.0.0/0", gateway_id=internet_gateway.id
        )
    ],
)

public_subnet_rt_association = aws.ec2.RouteTableAssociation(
    "public_subnet_rt_association",
    subnet_id=public_subnet.id,
    route_table_id=public_subnet_route_table.id,
)