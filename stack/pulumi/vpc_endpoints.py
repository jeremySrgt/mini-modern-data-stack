from typing import List
import pulumi_aws as aws

from security_groups import sg_allow_443_inbound_from_referenced_sg, sg_ssm
from network.vpc import data_vpc
from network.private_subnets import private_subnet


def ssm_vpc_endpoints(
    vpc_id: str, sg_ids: List[str], subnet_ids: List[str]
) -> List[aws.ec2.VpcEndpoint]:
    service_names = [
        "com.amazonaws.eu-west-3.ssm",
        "com.amazonaws.eu-west-3.ssmmessages",
        "com.amazonaws.eu-west-3.ec2messages",
    ]
    endpoints = []

    for service in service_names:
        resource_name = f"vpc_endpoint_{service.split('.')[-1]}"
        endpoints.append(
            aws.ec2.VpcEndpoint(
                resource_name,
                service_name=service,
                ip_address_type="ipv4",
                private_dns_enabled=True,
                vpc_id=vpc_id,
                auto_accept=True,
                security_group_ids=sg_ids,
                subnet_ids=subnet_ids,
                vpc_endpoint_type="Interface",
                tags={"Name": resource_name, "env": "dev"},
            )
        )

    return endpoints

vpc_endpoint_sg = sg_allow_443_inbound_from_referenced_sg(
    resource_name="sg_allow_443_inbound_from_referenced_sg",
    vpc_id=data_vpc.id,
    reference_sg_id=sg_ssm.id,
)

vpc_endpoints = ssm_vpc_endpoints(
    vpc_id=data_vpc.id, sg_ids=[vpc_endpoint_sg.id], subnet_ids=[private_subnet.id]
)