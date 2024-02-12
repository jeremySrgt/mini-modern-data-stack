import json
import pulumi_aws as aws

data_ecr = aws.ecr.Repository(
    "data_job_image_repository",
    name="data_job",
    image_scanning_configuration=aws.ecr.RepositoryImageScanningConfigurationArgs(
        scan_on_push=True,
    ),
    image_tag_mutability="MUTABLE",  # Should be immutable but for simplicity we will stick to immutable
    force_delete=True,
    encryption_configurations=[
        aws.ecr.RepositoryEncryptionConfigurationArgs(encryption_type="KMS")
    ],
    tags={"Name": "data_job", "env": "dev"},
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
