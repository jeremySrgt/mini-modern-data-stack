import json
import pulumi
import pulumi_aws as aws

from typing import Tuple
from jobs.ecs_cluster import ecs_task_role, data_ecs_cluster
from jobs.cloudwatch import cloudwatch_ecs_role, cloudwatch_ecs_log_group
from jobs.ecr import data_jobs_image
from jobs.config import ENV
from network.private_subnets import private_subnet
from instance.security_groups import allow_outbound_to_anywhere


def create_ecs_task_definition(
        name: str, file_name: str, memory: str, cpu: str
) -> aws.ecs.TaskDefinition:
    task_definition = aws.ecs.TaskDefinition(
        f"{name}",
        container_definitions=pulumi.Output.all(
            data_jobs_image.image_uri, cloudwatch_ecs_log_group.name
        ).apply(
            lambda args: json.dumps(
                [
                    {
                        "name": f"{name}",
                        "image": f"{args[0]}",
                        "essential": True,
                        "command": ["python", f"jobs/{file_name}"],
                        "environment": [
                            {"name": "DATAWAREHOUSE_DB", "value": "datawarehouse"},
                        ],
                        # "secrets": [
                        #     {
                        #         "name": "DATAWAREHOUSE_PASSWORD",
                        #         "valueFrom": "<secret_arn>:<secret_key>::",
                        #     },
                        # ],
                        "logConfiguration": {
                            "logDriver": "awslogs",
                            "options": {
                                "awslogs-group": f"{args[1]}",
                                "awslogs-region": "eu-west-3",
                                "awslogs-stream-prefix": "ecs",
                            },
                        },
                    }
                ]
            )
        ),
        runtime_platform=aws.ecs.TaskDefinitionRuntimePlatformArgs(
            cpu_architecture="X86_64"
        ),
        family=f"{name}",
        cpu=cpu,
        memory=memory,
        network_mode="awsvpc",
        requires_compatibilities=["FARGATE"],
        execution_role_arn=ecs_task_role.arn,
        tags={"Name": f"{ENV}-{name}-task-def", "env": ENV},
    )

    return task_definition


def create_cloudwatch_event_rule(
        name: str, schedule: str, task: aws.ecs.TaskDefinition, state: str
) -> Tuple[aws.cloudwatch.EventRule, aws.cloudwatch.EventTarget]:
    cw_event_rule = aws.cloudwatch.EventRule(
        f"{name}_cw_rule",
        description=f"CloudWatch event rule for job {name}",
        name=f"{name}_cw_rule",
        role_arn=cloudwatch_ecs_role.arn,
        schedule_expression=schedule,
        state=state,
        tags={"Name": f"{ENV}-{name}-event-rule", "env": ENV},
    )

    cw_event_target = aws.cloudwatch.EventTarget(
        f"{name}_cw_target",
        rule=cw_event_rule.id,
        arn=data_ecs_cluster.arn,
        role_arn=cloudwatch_ecs_role.arn,
        target_id=data_ecs_cluster.name,
        ecs_target=aws.cloudwatch.EventTargetEcsTargetArgs(
            task_definition_arn=task.arn,
            launch_type="FARGATE",
            network_configuration=aws.cloudwatch.EventTargetEcsTargetNetworkConfigurationArgs(
                subnets=[private_subnet.id],
                security_groups=[allow_outbound_to_anywhere.id],
                assign_public_ip=False,
            ),
        ),
    )

    return cw_event_rule, cw_event_target


def create_scheduled_job(
        name: str,
        file_name: str,
        schedule: str,
        memory: str = "1024",
        cpu: str = "512",
        is_enabled: bool = True,
) -> None:
    state = "ENABLED" if is_enabled else "DISABLED"
    task = create_ecs_task_definition(
        name=name, file_name=file_name, memory=memory, cpu=cpu
    )
    create_cloudwatch_event_rule(name=name, schedule=schedule, task=task, state=state)
