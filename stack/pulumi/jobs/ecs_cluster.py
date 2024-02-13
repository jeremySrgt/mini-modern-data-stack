import pulumi_aws as aws
import json

from jobs.config import ENV

data_ecs_cluster = aws.ecs.Cluster(
    "data_ecs_cluster",
    name=f"{ENV}-data-ecs-cluster",
    settings=[
        aws.ecs.ClusterSettingArgs(
            name="containerInsights",
            value="enabled",
        )
    ],
    tags={"Name": f"{ENV}-data-ecs-cluster", "env": ENV},
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
    tags={"Name": f"{ENV}-ecs-task-role", "env": ENV},
)


ecs_task_policy_attach = aws.iam.RolePolicyAttachment(
    "ecs_task_policy_attach",
    role=ecs_task_role.name,
    policy_arn="arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy",
)

# If you pass Secret Manager secret to your fargate task, you need this policy to retrieve them

# ecs_task_policy_secret_manager = aws.iam.Policy(
#     "ecs_task_policy_secret_manager",
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

# ecs_task_secret_manager_policy_attach = aws.iam.RolePolicyAttachment(
#     "ecs_task_secret_manager_allow_policy_attach",
#     role=ecs_task_role.name,
#     policy_arn=ecs_task_policy_secret_manager.arn,
# )
