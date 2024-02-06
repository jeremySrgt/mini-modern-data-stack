import pulumi
import instance
import network
import security_groups
import vpc_endpoints
import data_warehouse

cfg = pulumi.Config()

metabase_instance = instance.ec2_instance(
    resource_name="metabase_instance",
    instance_type=cfg.require("metabase_instance_type"),
    az="eu-west-3a",
    subnet_id=network.private_subnet.id,
    security_group_ids=[security_groups.sg_ssm.id]
)

airbyte_instance = instance.ec2_instance(
    resource_name="airbyte_instance",
    instance_type=cfg.require("airbyte_instance_type"),
    az="eu-west-3a",
    subnet_id=network.private_subnet.id,
    security_group_ids=[security_groups.sg_ssm.id]
)
