import pulumi
import pulumi_aws as aws
from network import warehouse_subnet_group, data_vpc

cfg = pulumi.Config()

data_warehouse_sg = aws.ec2.SecurityGroup(
    "data_warehouse_sg",
    description="Allow inbound traffic only if it is coming from instance inside our vpc",
    vpc_id=data_vpc.id,
    tags={"Name": "data-warehouse-sg", "env": "dev"},
)

data_warehouse_sg_ingress_rule = aws.vpc.SecurityGroupIngressRule(
    "data_warehouse_sg_ingress_rule",
    security_group_id=data_warehouse_sg.id,
    from_port=5432,
    to_port=5432,
    ip_protocol="tcp",
    cidr_ipv4="10.0.2.0/24",  # Change this once we have ou instance attached SG as ingress source
)

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