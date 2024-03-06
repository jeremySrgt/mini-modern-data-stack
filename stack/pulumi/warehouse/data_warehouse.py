import pulumi_aws as aws
from warehouse.subnet_groups import warehouse_subnet_group
from warehouse.security_groups import allow_5432_inbound_from_private_subnet
from network.az import primary_az
from warehouse.config import (
    ENV,
    DATA_WAREHOUSE_MASTER_USER,
    DATA_WAREHOUSE_MASTER_PASSWORD,
    WAREHOUSE_INSTANCE_CLASS,
    WAREHOUSE_DB_NAME,
)

data_warehouse = aws.rds.Instance(
    "data_warehouse",
    instance_class=WAREHOUSE_INSTANCE_CLASS,
    allocated_storage=20,
    allow_major_version_upgrade=False,
    auto_minor_version_upgrade=True,
    availability_zone=primary_az,
    backup_retention_period=1,
    backup_window="23:00-23:30",
    db_name=WAREHOUSE_DB_NAME,
    db_subnet_group_name=warehouse_subnet_group.name,
    engine="postgres",
    engine_version="14",
    identifier=f"{ENV}-data-warehouse-rds-instance",
    maintenance_window="thu:02:00-thu:05:00",
    max_allocated_storage=0,
    multi_az=False,
    publicly_accessible=False,
    skip_final_snapshot=True,
    storage_encrypted=True,
    storage_type="gp2",
    username=DATA_WAREHOUSE_MASTER_USER,
    password=DATA_WAREHOUSE_MASTER_PASSWORD,
    vpc_security_group_ids=[allow_5432_inbound_from_private_subnet.id],
    tags={"Name": f"{ENV}-data-warehouse-rds", "env": ENV},
)
