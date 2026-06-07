from extensions import db


class MasterIngredient(db.Model):

    __tablename__ = "master_ingredients"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(255),
        unique=True,
        nullable=False
    )

    is_flour = db.Column(
        db.Boolean,
        default=False
    )

    is_liquid = db.Column(
        db.Boolean,
        default=False
    )


    def __repr__(self):
        return f"<MasterIngredient {self.name}>"