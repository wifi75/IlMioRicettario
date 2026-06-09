from datetime import datetime
from extensions import db

# Tabella di associazione Many-to-Many tra Ricette e Teglie abilitate
recipe_pans = db.Table(
    "recipe_pans",
    db.Column("recipe_id", db.Integer, db.ForeignKey("recipes.id", ondelete="CASCADE"), primary_key=True),
    db.Column("pan_id", db.Integer, db.ForeignKey("master_bakery_pans.id", ondelete="CASCADE"), primary_key=True)
)


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

    # --- NUOVO CAMPO TESTO BADGE PERSONALIZZATO ---
    badge_text = db.Column(
        db.String(100),
        nullable=True,
        default="Antica Formula Bilanciata"
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

    # --- SOTTO-SISTEMA DI VISIBILITÀ CON SWITCH BOOLEANI ---
    show_chiusura = db.Column(
        db.Boolean,
        default=True
    )

    show_autolysis = db.Column(
        db.Boolean,
        default=True
    )

    show_puntata = db.Column(
        db.Boolean,
        default=True
    )

    puntata_fino_al_raddoppio = db.Column(
        db.Boolean,
        default=False
    )

    show_appretto = db.Column(
        db.Boolean,
        default=True
    )

    # --- GESTIONE AVANZATA PREFERMENTAZIONE (FASE 1) ---
    fermentation_type = db.Column(
        db.String(50),
        nullable=False,
        default="diretto"  # 'diretto', 'poolish', 'biga'
    )

    preferment_instructions = db.Column(
        db.Text,
        nullable=True
    )

    # --- RATIO CONVERSIONE LIEVITO PERSONALIZZATO RICETTA ---
    yeast_ratio = db.Column(
        db.Float,
        nullable=False,
        default=3.0
    )

    # --- NUOVI CAMPI DI MEMORIZZAZIONE VALORI LIEVITO LETTERALI UTENTE ---
    yeast_fresh_saved = db.Column(
        db.Float,
        nullable=True,
        default=3.0
    )

    yeast_dry_saved = db.Column(
        db.Float,
        nullable=True,
        default=1.0
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

    # --- RELAZIONI E COLLEGAMENTI ---
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

    # Relazione Many-to-Many con la flotta delle teglie master infinite
    pans = db.relationship(
        "MasterBakeryPan",
        secondary=recipe_pans,
        lazy="subquery",
        backref=db.backref("recipes", lazy=True)
    )


    def ingredient_count(self):
        return len(self.ingredients)


    def total_flour(self):
        return sum(
            ingredient.quantity
            for ingredient in self.ingredients
            for ingredient_master in [getattr(ingredient, 'master_ingredient', None)]
            if (ingredient_master and ingredient_master.is_flour) or getattr(ingredient, 'is_flour', False)
        )


    def total_liquids(self):
        return sum(
            ingredient.quantity
            for ingredient in self.ingredients
            for ingredient_master in [getattr(ingredient, 'master_ingredient', None)]
            if (ingredient_master and ingredient_master.is_liquid) or getattr(ingredient, 'is_liquid', False)
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