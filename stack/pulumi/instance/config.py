from pulumi import Config

cfg = Config()

ENV = cfg.require("env")
PUBLIC_KEY_PATH = cfg.require("public_key_path")
