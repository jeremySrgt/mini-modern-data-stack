from pulumi import Config

cfg = Config()

ENV = cfg.get("env", default="dev")
WAREHOUSE_INSTANCE_CLASS = cfg.get("warehouse_instance_class", default="db.t3.micro")
WAREHOUSE_DB_NAME = cfg.get("warehouse_db_name", default="company_data_warehouse")
DATA_WAREHOUSE_MASTER_USER = cfg.require_secret("dwh_master_user")
DATA_WAREHOUSE_MASTER_PASSWORD = cfg.require_secret("dwh_master_password")
