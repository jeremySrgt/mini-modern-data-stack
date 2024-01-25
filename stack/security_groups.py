import pulumi_aws as aws


def sg_allow_443_outbound_to_cidr_block(
    resource_name, vpc_id: str, authorized_cidr_block: str
) -> aws.ec2.SecurityGroup:
    sg = aws.ec2.SecurityGroup(
        resource_name,
        description="Allow outbound traffic to vpc endpoint net work interface",
        vpc_id=vpc_id,
        tags={"Name": resource_name, "env": "dev"},
    )

    aws.vpc.SecurityGroupEgressRule(
        f"{resource_name}_egress_rule",
        security_group_id=sg.id,
        ip_protocol="tcp",
        cidr_ipv4=authorized_cidr_block,
        from_port=443,
        to_port=443,
    )

    return sg


def sg_allow_443_inbound_from_referenced_sg(
    resource_name: str, vpc_id: str, reference_sg_id: str
) -> aws.ec2.SecurityGroup:
    sg = aws.ec2.SecurityGroup(
        resource_name,
        description="Allow inbound traffic from referenced SG",
        vpc_id=vpc_id,
        tags={"Name": resource_name, "env": "dev"},
    )

    aws.vpc.SecurityGroupIngressRule(
        f"{resource_name}_ingress_rule",
        security_group_id=sg.id,
        ip_protocol="tcp",
        referenced_security_group_id=reference_sg_id,
        from_port=443,
        to_port=443,
    )

    return sg
