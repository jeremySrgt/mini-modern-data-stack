from pulumi import Config

cfg = Config()

ENV = cfg.require("env")
