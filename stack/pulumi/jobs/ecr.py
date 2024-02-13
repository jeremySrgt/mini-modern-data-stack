import json
import pulumi_aws as aws
import pulumi_awsx as awsx
from jobs.config import ENV

data_ecr = aws.ecr.Repository(
    "data_job_image_repository",
    name="data_jobs",
    image_scanning_configuration=aws.ecr.RepositoryImageScanningConfigurationArgs(
        scan_on_push=True,
    ),
    image_tag_mutability="IMMUTABLE",
    force_delete=True,
    encryption_configurations=[
        aws.ecr.RepositoryEncryptionConfigurationArgs(encryption_type="KMS")
    ],
    tags={"Name": f"{ENV}-data-jobs-ecr", "env": ENV},
)

aws.ecr.LifecyclePolicy(
    "data_ecr_lifecycle_policy",
    repository=data_ecr.name,
    policy=json.dumps(
        {
            "rules": [
                {
                    "rulePriority": 1,
                    "description": "Keep last 30 images",
                    "selection": {
                        "tagStatus": "any",
                        "countType": "imageCountMoreThan",
                        "countNumber": 30,
                    },
                    "action": {"type": "expire"},
                }
            ]
        }
    ),
)

data_jobs_image = awsx.ecr.Image(
    "data_jobs_image",
    repository_url=data_ecr.repository_url,
    context="../data_jobs",
    platform="linux/x86_64",
)
