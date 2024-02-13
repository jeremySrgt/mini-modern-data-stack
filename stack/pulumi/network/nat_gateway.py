import pulumi_aws as aws
from network.public_subnets import public_subnet
from network.config import ENV

nat_gateway_eip = aws.ec2.Eip(
    "nat_gateway_eip", tags={"Name": f"{ENV}-nat-gateway-eip", "env": ENV}
)

nat_gateway = aws.ec2.NatGateway(
    "nat_gateway",
    allocation_id=nat_gateway_eip.id,
    subnet_id=public_subnet.id,
    tags={"Name": f"{ENV}-data_nat_gateway", "env": ENV},
)
