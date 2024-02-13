import pulumi_aws as aws
from network.config import ENV

data_vpc = aws.ec2.Vpc(
    "data_vpc",
    cidr_block="10.0.0.0/16",
    enable_dns_hostnames=True,
    enable_dns_support=True,
    tags={"Name": f"{ENV}-mini-data-stack", "env": ENV},
)

internet_gateway = aws.ec2.InternetGateway(
    "internet_gateway",
    vpc_id=data_vpc.id,
    tags={"Name": f"{ENV}-internet-gateway", "env": ENV},
)