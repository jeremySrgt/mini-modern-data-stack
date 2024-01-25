import pulumi
import pulumi_aws as aws
import json

cfg = pulumi.Config()

data_vpc = aws.ec2.Vpc(
    "data_vpc",
    cidr_block="10.0.0.0/16",
    enable_dns_hostnames=True,
    enable_dns_support = True,
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


def ec2_role_instance_profile() -> aws.iam.InstanceProfile:
    ec2_instance_role = aws.iam.Role(
        "ec2--instance-role",
        name="ec2-instance-role",
        assume_role_policy=json.dumps(
            {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Action": "sts:AssumeRole",
                        "Principal": {"Service": "ec2.amazonaws.com"},
                        "Effect": "Allow",
                        "Sid": "",
                    }
                ],
            }
        ),
    )

    aws.iam.RolePolicyAttachment(
        "ec2-instance-role-policy-attachment-ssm-role",
        role=ec2_instance_role.name,
        policy_arn="arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore",
    )

    ec2_instance_profile = aws.iam.InstanceProfile(
        "ec2-instance-profile",
        name="ec2-instance-profile",
        role=ec2_instance_role.name,
    )

    return ec2_instance_profile


ec2_sg = aws.ec2.SecurityGroup(
    "ec2_sg",
    description="Allow outbound traffic to vpc endpoint net work interface",
    vpc_id=data_vpc.id,
    tags={"Name": "ec2-sg", "env": "dev"},
)

ec2_sg_egress_rule = aws.vpc.SecurityGroupEgressRule(
    "ec2_sg_egress_rule",
    security_group_id=ec2_sg.id,
    ip_protocol="-1",
    cidr_ipv4=private_subnet.cidr_block,
)

ec2_sg_ingress_rule = aws.vpc.SecurityGroupIngressRule(
    "ec2_sg_ingress_rule",
    security_group_id=ec2_sg.id,
    ip_protocol="-1",
    cidr_ipv4="0.0.0.0/0",
)

vpc_endpoint_sg = aws.ec2.SecurityGroup(
    "vpc_endpoint_sg",
    description="Allow inbound traffic from EC2 instance with attached SG",
    vpc_id=data_vpc.id,
    tags={"Name": "vpc-endpoint-sg", "env": "dev"},
)

vpc_endpoint_sg_ingress_rule = aws.vpc.SecurityGroupIngressRule(
    "vpc_endpoint_sg_ingress_rule",
    security_group_id=vpc_endpoint_sg.id,
    ip_protocol="tcp",
    cidr_ipv4=private_subnet.cidr_block,
    # referenced_security_group_id=ec2_sg.id,
    from_port=443,
    to_port=443,
)

vpc_endpoint_sg_egress_rule = aws.vpc.SecurityGroupEgressRule(
    "vpc_endpoint_sg_Egress_rule",
    security_group_id=vpc_endpoint_sg.id,
    ip_protocol="-1",
    cidr_ipv4="0.0.0.0/0",
)

vpc_endpoint_ssm = aws.ec2.VpcEndpoint(
    "vpc_endpoint_ssm",
    service_name="com.amazonaws.eu-west-3.ssm",
    ip_address_type="ipv4",
    private_dns_enabled=True,
    vpc_id=data_vpc.id,
    auto_accept=True,
    security_group_ids=[vpc_endpoint_sg.id],
    subnet_ids=[private_subnet.id],
    vpc_endpoint_type="Interface",
)

vpc_endpoint_ssm_messages = aws.ec2.VpcEndpoint(
    "vpc_endpoint_ssm_messages",
    service_name="com.amazonaws.eu-west-3.ssmmessages",
    ip_address_type="ipv4",
    private_dns_enabled=True,
    vpc_id=data_vpc.id,
    auto_accept=True,
    security_group_ids=[vpc_endpoint_sg.id],
    subnet_ids=[private_subnet.id],
    vpc_endpoint_type="Interface",
)

vpc_endpoint_ec2_messages = aws.ec2.VpcEndpoint(
    "vpc_endpoint_ec2_messages",
    service_name="com.amazonaws.eu-west-3.ec2messages",
    ip_address_type="ipv4",
    private_dns_enabled=True,
    vpc_id=data_vpc.id,
    auto_accept=True,
    security_group_ids=[vpc_endpoint_sg.id],
    subnet_ids=[private_subnet.id],
    vpc_endpoint_type="Interface",
)


def ec2_instance() -> aws.ec2.Instance:
    instance_profile = ec2_role_instance_profile()
    ec2_ecs_instance = aws.ec2.Instance(
        "ec2-instance",
        instance_type="t3.micro",
        ami="ami-0cb7af6ec2ad3c332",
        iam_instance_profile=instance_profile.name,
        availability_zone="eu-west-3a",
        subnet_id=private_subnet.id,
        vpc_security_group_ids=[ec2_sg.id],
        root_block_device=aws.ec2.InstanceRootBlockDeviceArgs(
            delete_on_termination=True,
            encrypted=True,
            volume_size=20,
            volume_type="gp3",
            tags={"Name": "ec2-attached-instance-volume", "env": "dev"},
        ),
        tags={"Name": "ec2-attached-instance", "env": "dev"},
    )

    return ec2_ecs_instance


ec2_instance()
