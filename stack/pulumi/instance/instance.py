import pulumi_aws as aws
from instance.instance_profile import ec2_instance_profile
from instance.security_groups import (
    allow_443_outbound_to_private_subnet_cidr,
    allow_outbound_to_anywhere,
)
from network.vpc import internet_gateway
from instance.config import ENV, PUBLIC_KEY_PATH

public_key = open(PUBLIC_KEY_PATH).read()

data_instance_keypair = aws.ec2.KeyPair(
    "data_instance_keypair",
    public_key=public_key,
    tags={"Name": f"{ENV}-data-instance-keypair", "env": ENV},
)


def ec2_instance(
        resource_name: str,
        subnet_id: str,
        instance_type: str,
        az: str,
) -> aws.ec2.Instance:
    instance = aws.ec2.Instance(
        resource_name,
        instance_type=instance_type,
        ami="ami-0cb7af6ec2ad3c332",
        iam_instance_profile=ec2_instance_profile.name,
        availability_zone=az,
        subnet_id=subnet_id,
        vpc_security_group_ids=[
            allow_443_outbound_to_private_subnet_cidr.id,
            allow_outbound_to_anywhere.id,
        ],
        key_name=data_instance_keypair.id,
        root_block_device=aws.ec2.InstanceRootBlockDeviceArgs(
            delete_on_termination=False,
            # To keep Metabase and Airbyte data in case you didn't setup a proper persistent storage for them, like a db
            encrypted=True,
            volume_size=20,
            volume_type="gp3",
            tags={"Name": f"{ENV}-{resource_name}-volume", "env": ENV},
        ),
        tags={"Name": f"{ENV}-{resource_name}", "env": ENV},
    )

    return instance
