from extensions import db


class MasterBakeryPan(db.Model):

    __tablename__ = "master_bakery_pans"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    pan_type = db.Column(
        db.String(50),
        nullable=False,
        default="rettangolare"  # Accetta: 'rettangolare', 'rotonda', 'stampo'
    )

    weight_capacity = db.Column(
        db.Float,
        nullable=False,
        default=0.0  # Grammi di impasto standard ottimale per questa teglia
    )


    def __repr__(self):
        return f"<MasterBakeryPan {self.name} ({self.weight_capacity}g)>"