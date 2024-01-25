import json
import pulumi_aws as aws

def ec2_instance_profile() -> aws.iam.InstanceProfile:
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

instance_profile = ec2_instance_profile()