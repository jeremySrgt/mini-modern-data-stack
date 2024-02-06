import instance
import network
import security_groups
import vpc_endpoints
import data_warehouse


test_instance = instance.ec2_instance(
    resource_name="test-instance",
    instance_type="t3.micro",
    az="eu-west-3a",
    subnet_id=network.private_subnet.id,
    security_group_ids=[security_groups.sg_ssm.id]
)
