import pulumi
import instance
import security_groups
import vpc_endpoints
import data_warehouse
import ecr
import ecs_cluster
import pulumi_aws as aws
from scheduled_job import create_scheduled_job
from network.private_subnets import private_subnet

cfg = pulumi.Config()

public_key_path = cfg.require("public_key_path")

public_key = open(public_key_path).read()

data_instance_keypair = aws.ec2.KeyPair("data_instance_keypair", public_key=public_key)

metabase_instance = instance.ec2_instance(
    resource_name="metabase_instance",
    instance_type=cfg.require("metabase_instance_type"),
    az="eu-west-3a",
    subnet_id=private_subnet.id,
    security_group_ids=[
        security_groups.sg_ssm.id,
        security_groups.sg_allow_outbound_to_anywhere,
    ],
    keypair_id=data_instance_keypair.id,
)

airbyte_instance = instance.ec2_instance(
    resource_name="airbyte_instance",
    instance_type=cfg.require("airbyte_instance_type"),
    az="eu-west-3a",
    subnet_id=private_subnet.id,
    security_group_ids=[
        security_groups.sg_ssm.id,
        security_groups.sg_allow_outbound_to_anywhere,
    ],
    keypair_id=data_instance_keypair.id,
)

create_scheduled_job(
    name="hello_jobs",
    file_name="hello_jobs.py",
    schedule="cron(30 6 * * ? *)",  # Every day at 6.30 AM UTC
)

