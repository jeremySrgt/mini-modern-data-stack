from pulumi import Config

cfg = Config()

ENV = cfg.get("env", default="dev")
