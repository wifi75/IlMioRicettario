import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")

    if not SECRET_KEY:
        raise RuntimeError(
            "Variabile d'ambiente SECRET_KEY non impostata. "
            "Aggiungila al file .service di systemd nella sezione [Service]."
        )

    SQLALCHEMY_DATABASE_URI = (
        f"sqlite:///{os.path.join(BASE_DIR, 'data', 'database.db')}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
