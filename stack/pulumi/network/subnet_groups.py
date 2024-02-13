import pulumi_aws as aws
from network.private_subnets import private_subnet, private_subnet_2
from network.config import ENV

warehouse_subnet_group = aws.rds.SubnetGroup(
    "data_warehouse_subnet_group",
    subnet_ids=[private_subnet.id, private_subnet_2.id],
    tags={"Name": f"{ENV}-data-warehouse-subnet-group", "env": ENV},
)
