import json
import pulumi_aws as aws
from jobs.config import ENV

cloudwatch_ecs_log_group = aws.cloudwatch.LogGroup(
    "cloudwatch_ecs_log_group",
    name=f"{ENV}-ecs-log-group",
    retention_in_days=30,
    tags={"Name": f"{ENV}-ecs-log-group", "env": ENV},
)

cloudwatch_ecs_role = aws.iam.Role(
    "cloudwatch_ecs_role",
    assume_role_policy=json.dumps(
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "sts:AssumeRole",
                    "Effect": "Allow",
                    "Sid": "",
                    "Principal": {"Service": "ecs-tasks.amazonaws.com"},
                },
                {
                    "Action": "sts:AssumeRole",
                    "Effect": "Allow",
                    "Sid": "",
                    "Principal": {"Service": "events.amazonaws.com"},
                },
            ],
        }
    ),
    tags={"Name": f"{ENV}-ecs-cw-role", "env": ENV},
)

cloudwatch_managed_policy_attach = aws.iam.RolePolicyAttachment(
    "cloudwatch_managed_policy_attach",
    role=cloudwatch_ecs_role.name,
    policy_arn="arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceEventsRole",
)


def cloud_watch_pass_role_policy(task_role_arn):
    return (
        json.dumps(
            {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Action": ["iam:PassRole"],
                        "Effect": "Allow",
                        "Resource": [task_role_arn],
                    }
                ],
            }
        ),
    )


cloud_watch_policy = aws.iam.Policy(
    "cloudwatch_policy_pass_role",
    description="Cloudwatch passRole for ecs task policy",
    policy=json.dumps(
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": ["iam:PassRole"],
                    "Effect": "Allow",
                    "Resource": "*",
                }
            ],
        }
    ),
)

# Attach CloudWatch Policy
cloudwatch_policy_attach = aws.iam.RolePolicyAttachment(
    "cloudwatch_pass_role_policy_attach",
    role=cloudwatch_ecs_role.name,
    policy_arn=cloud_watch_policy.arn,
)
