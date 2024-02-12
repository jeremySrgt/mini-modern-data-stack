import pulumi_aws as aws
import json

data_ecs_cluster = aws.ecs.Cluster(
    "data_ecs_cluster",
    name="data_ecs_cluster",
    settings=[
        aws.ecs.ClusterSettingArgs(
            name="containerInsights",
            value="enabled",
        )
    ],
    tags={"Name": "data_ecs_cluster", "env": "dev"},
)

cloudwatch_ecs_log_group = aws.cloudwatch.LogGroup(
    "cloudwatch_ecs_log_group",
    name="ecs_log_group",
    retention_in_days=30,
    tags={"Name": "ecs_log_group", "env": "dev"},
)


ecs_task_role = aws.iam.Role(
    "ecs_task_role",
    assume_role_policy=json.dumps(
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "sts:AssumeRole",
                    "Effect": "Allow",
                    "Sid": "",
                    "Principal": {"Service": "ecs-tasks.amazonaws.com"},
                }
            ],
        }
    ),
    tags={"Name": "ecs-task-role", "env": "dev"},
)


ecs_task_policy_attach = aws.iam.RolePolicyAttachment(
    "ecs_task_policy_attach",
    role=ecs_task_role.name,
    policy_arn="arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy",
)

# If you pass Secret Manager secret to your fargate task, you need this policy to retrieve them

# ecs_task_policy = aws.iam.Policy(
#     "ecs-task-policy",
#     description="Authorize ECS task to retrieve secret from secret manager",
#     policy=json.dumps(
#         {
#             "Version": "2012-10-17",
#             "Statement": [
#                 {
#                     "Effect": "Allow",
#                     "Action": ["secretsmanager:GetSecretValue"],
#                     "Resource": ["<secret_arn>"],
#                 }
#             ],
#         }
#     ),
# )

# ecs_task_sm_allow_policy_attach = aws.iam.RolePolicyAttachment(
#     "ecs_task_sm_allow_policy_attach",
#     role=ecs_task_role.name,
#     policy_arn=ecs_task_policy.arn,
# )

# CloudWatch Role
cloudwatch_role = aws.iam.Role(
    "cloudwatch_role",
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
    tags={"Name": "ecs-cw-task-role", "env": "dev"},
)

cloudwatch_managed_policy_attach = aws.iam.RolePolicyAttachment(
    "cloudwatch_managed_policy_attach",
    role=cloudwatch_role.name,
    policy_arn="arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceEventsRole",
)


# pass task role to the json
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
    "cloudwatch-policy-pass-role-cw",
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
    "cloudwatch_policy_attach",
    role=cloudwatch_role.name,
    policy_arn=cloud_watch_policy.arn,
)
