from pulumi import Config

cfg = Config()

METABASE_INSTANCE_TYPE = cfg.get("metabase_instance_type", default="t3.micro")
AIRBYTE_INSTANCE_TYPE = cfg.get("airbyte_instance_type", default="t3.medium")
