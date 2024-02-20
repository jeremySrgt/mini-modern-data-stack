import pulumi_aws as aws
from network.vpc import data_vpc
from network.nat_gateway import nat_gateway
from network.config import ENV

available_az = aws.get_availability_zones(state="available")
primary_az = available_az.names[0]
secondary_az = available_az.names[1]

private_subnet = aws.ec2.Subnet(
    "private_subnet",
    vpc_id=data_vpc.id,
    availability_zone=primary_az,
    cidr_block="10.0.2.0/24",
    map_public_ip_on_launch=False,
    tags={"Name": f"{ENV}-data-private-subnet", "env": ENV},
)

private_subnet_route_table = aws.ec2.RouteTable(
    "private_subnet_route_table",
    vpc_id=data_vpc.id,
    routes=[
        aws.ec2.RouteTableRouteArgs(
            cidr_block="0.0.0.0/0", nat_gateway_id=nat_gateway.id
        )
    ],
    tags={"Name": f"{ENV}-private-subnet-rt", "env": ENV},
)

private_subnet_rt_association = aws.ec2.RouteTableAssociation(
    "private_subnet_rt_association",
    subnet_id=private_subnet.id,
    route_table_id=private_subnet_route_table.id,
)

private_subnet_2 = aws.ec2.Subnet(
    "private_subnet_2",
    vpc_id=data_vpc.id,
    availability_zone=secondary_az,
    cidr_block="10.0.3.0/24",
    map_public_ip_on_launch=False,
    tags={"Name": f"{ENV}-data-private-subnet-2", "env": ENV},
)
