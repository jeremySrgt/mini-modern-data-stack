import pulumi
import warehouse.data_warehouse as data_warehouse
import jobs.ecr as ecr
import jobs.ecs_cluster as ecs_cluster
import network.vpc_endpoints
from jobs.scheduled_job import create_scheduled_job
from network.private_subnets import private_subnet
from instance.instance import ec2_instance
from config import METABASE_INSTANCE_TYPE, AIRBYTE_INSTANCE_TYPE


metabase_instance = ec2_instance(
    resource_name="metabase_instance",
    instance_type=METABASE_INSTANCE_TYPE,
    az="eu-west-3a",
    subnet_id=private_subnet.id,
)

airbyte_instance = ec2_instance(
    resource_name="airbyte_instance",
    instance_type=AIRBYTE_INSTANCE_TYPE,
    az="eu-west-3a",
    subnet_id=private_subnet.id,
)

create_scheduled_job(
    name="hello_jobs",
    file_name="hello_jobs.py",
    schedule="cron(30 6 * * ? *)",  # Every day at 6.30 AM UTC
)


pulumi.export("Metabase instance ID", metabase_instance.id)
pulumi.export("Airbyte instance ID", airbyte_instance.id)
