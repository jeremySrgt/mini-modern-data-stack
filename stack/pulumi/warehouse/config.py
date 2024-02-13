from pulumi import Config

cfg = Config()

ENV = cfg.require("env")
WAREHOUSE_INSTANCE_CLASS = cfg.require("warehouse_instance_class")
WAREHOUSE_DB_NAME = cfg.require("warehouse_db_name")
DATA_WAREHOUSE_MASTER_USER = cfg.require_secret("dwh_master_user")
DATA_WAREHOUSE_MASTER_PASSWORD = cfg.require_secret("dwh_master_password")
