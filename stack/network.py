import pulumi_aws as aws

data_vpc = aws.ec2.Vpc(
    "data_vpc",
    cidr_block="10.0.0.0/16",
    enable_dns_hostnames=True,
    enable_dns_support=True,
    tags={"Name": "mini-data-stack", "env": "dev"},
)

public_subnet = aws.ec2.Subnet(
    "public_subnet",
    vpc_id=data_vpc.id,
    availability_zone="eu-west-3a",
    cidr_block="10.0.1.0/24",
    map_public_ip_on_launch=True,
    tags={"Name": "data-public-subnet", "env": "dev"},
)

private_subnet = aws.ec2.Subnet(
    "private_subnet",
    vpc_id=data_vpc.id,
    availability_zone="eu-west-3a",
    cidr_block="10.0.2.0/24",
    map_public_ip_on_launch=False,
    tags={"Name": "data-private-subnet", "env": "dev"},
)

private_subnet_2 = aws.ec2.Subnet(
    "private_subnet_2",
    vpc_id=data_vpc.id,
    availability_zone="eu-west-3b",
    cidr_block="10.0.3.0/24",
    map_public_ip_on_launch=False,
    tags={"Name": "data-private-subnet-2", "env": "dev"},
)

warehouse_subnet_group = aws.rds.SubnetGroup(
    "data_warehouse_subnet_group",
    subnet_ids=[private_subnet.id, private_subnet_2.id],
    tags={"Name": "data-warehouse-subnet-group", "env": "env"},
)