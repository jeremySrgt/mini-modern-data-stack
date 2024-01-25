from typing import List
import pulumi_aws as aws


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
