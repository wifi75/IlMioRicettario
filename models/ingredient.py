from extensions import db


class RecipeIngredient(db.Model):

    __tablename__ = "recipe_ingredients"

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
        db.String(255),
        nullable=False
    )

    quantity = db.Column(
        db.Float,
        nullable=False,
        default=0
    )

    percentage = db.Column(
        db.Float,
        default=0
    )

    unit = db.Column(
        db.String(20),
        default="g"
    )

    is_flour = db.Column(
        db.Boolean,
        default=False
    )

    is_liquid = db.Column(
        db.Boolean,
        default=False
    )

    # NUOVA COLONNA TECNICA LOCALIZZATA PER LA FORZA DELLE FARINE
    w_value = db.Column(
        db.Integer,
        nullable=True,
        default=0
    )

    is_optional = db.Column(
        db.Boolean,
        default=False
    )

    sort_order = db.Column(
        db.Integer,
        default=0
    )

    notes = db.Column(
        db.String(255)
    )

    def display_value(self):
        if self.percentage and self.percentage > 0:
            return f"{self.percentage}%"
        return f"{self.quantity} {self.unit}"

    def __repr__(self):
        return f"<Ingredient {self.name}>"