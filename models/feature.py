from extensions import db


class RecipeFeature(db.Model):

    __tablename__ = "recipe_features"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    recipe_id = db.Column(
        db.Integer,
        db.ForeignKey("recipes.id"),
        nullable=False,
        unique=True
    )

    enable_piece_count = db.Column(
        db.Boolean,
        default=False
    )

    enable_piece_weight = db.Column(
        db.Boolean,
        default=False
    )

    enable_hydration = db.Column(
        db.Boolean,
        default=False
    )

    enable_yeast_type = db.Column(
        db.Boolean,
        default=False
    )

    enable_tangzhong = db.Column(
        db.Boolean,
        default=False
    )

    enable_poolish = db.Column(
        db.Boolean,
        default=False
    )

    enable_biga = db.Column(
        db.Boolean,
        default=False
    )

    enable_sourdough = db.Column(
        db.Boolean,
        default=False
    )

    enable_baker_percentage = db.Column(
        db.Boolean,
        default=True
    )

    def __repr__(self):

        return (
            f"<RecipeFeature "
            f"recipe={self.recipe_id}>"
        )