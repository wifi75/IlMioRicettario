from extensions import db


class Setting(db.Model):

    __tablename__ = "settings"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    fresh_to_dry_ratio = db.Column(
        db.Float,
        default=3.0
    )

    tangzhong_flour_percent = db.Column(
        db.Float,
        default=5.0
    )

    tangzhong_liquid_multiplier = db.Column(
        db.Float,
        default=5.0
    )

    site_name = db.Column(
        db.String(100),
        default="Il Mio Ricettario"
    )

    default_unit = db.Column(
        db.String(20),
        default="g"
    )

    allow_public_recipes = db.Column(
        db.Boolean,
        default=True
    )

    # LA COLONNA AGGIUNTA SULLA TABELLA PLURALE CORRETTA
    theme_active = db.Column(
        db.String(50),
        default="modern"
    )

    def __repr__(self):
        return "<Settings>"