import os
import importlib.util

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
_INSTANCE_CFG = os.path.join(BASE_DIR, 'instance', 'config.py')


def _load_instance():
    if not os.path.exists(_INSTANCE_CFG):
        return {}
    spec = importlib.util.spec_from_file_location("_instance_cfg", _INSTANCE_CFG)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return {k: getattr(mod, k) for k in dir(mod) if not k.startswith('_')}


_inst = _load_instance()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or _inst.get("SECRET_KEY")

    if not SECRET_KEY:
        raise RuntimeError(
            "SECRET_KEY non configurata.\n"
            "Opzione 1 — file instance/config.py:  SECRET_KEY = \"la-tua-chiave\"\n"
            "Opzione 2 — variabile d'ambiente nel .service di systemd: Environment=\"SECRET_KEY=...\"\n"
            "Genera una chiave sicura con: python -c \"import secrets; print(secrets.token_hex(32))\""
        )

    PORT = int(_inst.get("PORT", os.environ.get("PORT", 8080)))

    SQLALCHEMY_DATABASE_URI = (
        f"sqlite:///{os.path.join(BASE_DIR, 'data', 'database.db')}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
