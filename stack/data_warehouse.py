import pulumi
import pulumi_aws as aws
from network import warehouse_subnet_group

cfg = pulumi.Config()

data_warehouse = aws.rds.Instance(
    "data_warehouse",
    instance_class="db.t3.micro",
    allocated_storage=20,
    allow_major_version_upgrade=False,
    auto_minor_version_upgrade=True,
    availability_zone="eu-west-3a",
    backup_retention_period=1,
    backup_window="23:00-23:30",
    db_name="company_datawarehouse",
    db_subnet_group_name=warehouse_subnet_group.name,
    engine="postgres",
    engine_version="14",
    identifier="data-warehouse-rds-instance",
    maintenance_window="thu:02:00-thu:05:00",
    max_allocated_storage=0,
    multi_az=False,
    publicly_accessible=False,
    skip_final_snapshot=True,
    storage_encrypted=True,
    storage_type="gp2",
    username=cfg.require_secret("dwh_master_user"),
    password=cfg.require_secret("dwh_master_password"),
    vpc_security_group_ids=[data_warehouse_sg.id],
    tags={"Name": "data-warehouse-rds", "env": "dev"},
)