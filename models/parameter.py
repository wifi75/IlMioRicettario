from extensions import db


class RecipeParameter(db.Model):

    __tablename__ = "recipe_parameters"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    recipe_id = db.Column(
        db.Integer,
        db.ForeignKey("recipes.id"),
        nullable=False
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    parameter_type = db.Column(
        db.String(50),
        nullable=False
    )

    default_value = db.Column(
        db.String(100)
    )

    min_value = db.Column(
        db.Float
    )

    max_value = db.Column(
        db.Float
    )

    options = db.Column(
        db.Text
    )

    sort_order = db.Column(
        db.Integer,
        default=0
    )

    def __repr__(self):

        return (
            f"<Parameter "
            f"{self.name}>"
        )