from pulumi import Config

cfg = Config()

METABASE_INSTANCE_TYPE = cfg.require("metabase_instance_type")
AIRBYTE_INSTANCE_TYPE = cfg.require("airbyte_instance_type")