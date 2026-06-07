from datetime import datetime

from extensions import db


class Recipe(db.Model):

    __tablename__ = "recipes"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(255),
        nullable=False
    )

    slug = db.Column(
        db.String(255),
        unique=True,
        nullable=False
    )

    description = db.Column(
        db.Text
    )

    instructions = db.Column(
        db.Text
    )

    image = db.Column(
        db.String(255)
    )

    icon = db.Column(
        db.String(50),
        nullable=False,
        default="bi-journal-text"
    )

    is_published = db.Column(
        db.Boolean,
        default=True
    )

    # --- NUOVI CAMPI PARAMETRI DI PROCESSO AVANZATI ---
    temp_chiusura = db.Column(
        db.Float,
        nullable=True,
        default=24.0
    )

    tempo_autolisi = db.Column(
        db.Integer,
        nullable=True,
        default=0
    )

    tempo_puntata = db.Column(
        db.Integer,
        nullable=True,
        default=120
    )

    tempo_appretto = db.Column(
        db.Integer,
        nullable=True,
        default=60
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    ingredients = db.relationship(
        "RecipeIngredient",
        backref="recipe",
        cascade="all, delete-orphan",
        lazy=True,
        order_by="RecipeIngredient.sort_order"
    )

    features = db.relationship(
        "RecipeFeature",
        backref="recipe",
        cascade="all, delete-orphan",
        lazy=True
    )


    def ingredient_count(self):
        return len(self.ingredients)


    def total_flour(self):

        return sum(
            ingredient.quantity
            for ingredient in self.ingredients
            if ingredient.is_flour
        )


    def total_liquids(self):

        return sum(
            ingredient.quantity
            for ingredient in self.ingredients
            if ingredient.is_liquid
        )


    def hydration(self):

        flour = self.total_flour()

        if flour <= 0:
            return 0

        return round(
            (self.total_liquids() / flour) * 100,
            1
        )


    def __repr__(self):
        return f"<Recipe {self.name}>"