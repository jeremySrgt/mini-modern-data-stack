from typing import List
import pulumi_aws as aws
from instance_profile import instance_profile


def ec2_instance(
    resource_name: str,
    subnet_id: str,
    instance_type: str,
    az: str,
    security_group_ids: List[str] = [],
) -> aws.ec2.Instance:

    ec2_ecs_instance = aws.ec2.Instance(
        resource_name,
        instance_type=instance_type,
        ami="ami-0cb7af6ec2ad3c332",
        iam_instance_profile=instance_profile.name,
        availability_zone=az,
        subnet_id=subnet_id,
        vpc_security_group_ids=security_group_ids,
        root_block_device=aws.ec2.InstanceRootBlockDeviceArgs(
            delete_on_termination=True,
            encrypted=True,
            volume_size=20,
            volume_type="gp3",
            tags={"Name": f"{resource_name}-volume", "env": "dev"},
        ),
        tags={"Name": resource_name, "env": "dev"},
    )

    return ec2_ecs_instance
