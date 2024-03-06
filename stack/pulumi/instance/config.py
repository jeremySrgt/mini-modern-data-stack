from pulumi import Config

cfg = Config()

ENV = cfg.get("env", default="dev")
PUBLIC_KEY_PATH = cfg.get("public_key_path", "../../dev-keypair.pub")
