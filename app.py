from flask import Flask
from flask import redirect
from flask import url_for

from werkzeug.security import generate_password_hash

from config import Config
from extensions import db
from extensions import login_manager

# IMPORTAZIONE STRUMENTO DI MIGRAZIONE PROFESSIONALE
from flask_migrate import Migrate

from models.user import User
from models.recipe import Recipe
from models.ingredient import RecipeIngredient
from models.feature import RecipeFeature
from models.setting import Setting
from models.wiki import WikiArticle
from models.parameter import RecipeParameter
from models.ingredient_master import MasterIngredient
# IMPORTAZIONE NUOVO MODELLO DELLE TEGLIE MASTER
from models.bakery_pan import MasterBakeryPan

from routes.recipes import recipes_bp
# BLINDATO: Forza il caricamento del Blueprint corretto per evitare conflitti di sotto-cartelle
from routes.admin import admin_bp


app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)
login_manager.init_app(app)

# INIZIALIZZAZIONE DEL MOTORE DI MIGRAZIONE DEL DATABASE
migrate = Migrate(app, db)

# ==========================================================
# CRITICO: NUOVO ORDINE DI REGISTRAZIONE BLUEPRINT
# ==========================================================
app.register_blueprint(admin_bp)
app.register_blueprint(recipes_bp)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(
        User,
        int(user_id)
    )


# CORRETTO: Ordiniamo per ID decrescente per prendere SICURAMENTE l'ultimo record attivo e aggiornato
@app.context_processor
def inject_global_settings():
    return dict(
        settings_data=Setting.query.order_by(Setting.id.desc()).first()
    )


@app.route("/")
def index():
    return redirect(
        url_for("recipes.list_recipes")
    )


with app.app_context():

    db.create_all()

    # =========================================================================
    # BLINDATURA STRUTTURALE ANTICRASH ANTICIPATA (SQL CRUDO A FREDDO)
    # Eseguiamo le alterazioni prima di qualsiasi interazione ORM
    # =========================================================================
    try:
        db.session.execute(db.text("ALTER TABLE settings ADD COLUMN theme_active VARCHAR(50) DEFAULT 'modern'"))
        db.session.commit()
    except Exception:
        db.session.rollback()

    try:
        db.session.execute(db.text("ALTER TABLE settings ADD COLUMN site_description TEXT"))
        db.session.commit()
        print("Allineamento Database: colonna 'site_description' verificata e inserita!")
    except Exception:
        db.session.rollback()

    try:
        db.session.execute(db.text("ALTER TABLE recipe_ingredients ADD COLUMN w_value INTEGER DEFAULT 0"))
        db.session.commit()
        print("Allineamento Ingredienti: colonna 'w_value' verificata e inserita con successo!")
    except Exception:
        db.session.rollback()

    # =========================================================================
    # DA QUI IN POI LE QUERY POSSONO GIRARE IN TOTALE SICUREZZA
    # =========================================================================
    admin = User.query.filter_by(
        username="admin"
    ).first()

    if not admin:

        admin = User(
            username="admin",
            password_hash=generate_password_hash(
                "admin123"
            ),
            is_admin=True
        )

        db.session.add(admin)
        db.session.commit()

        print("Admin creato")
        print("Username: admin")
        print("Password: admin123")

    if MasterBakeryPan.query.count() == 0:
        default_pans = [
            MasterBakeryPan(name="Teglia Rettangolare Ferro Blu 40x30", pan_type="rettangolare", weight_capacity=1200.0),
            MasterBakeryPan(name="Tonda Classica Diametro 32", pan_type="rotonda", weight_capacity=650.0),
            MasterBakeryPan(name="Stampo Panettone Alto 1kg", pan_type="stampo", weight_capacity=1000.0)
        ]
        db.session.bulk_save_objects(default_pans)
        db.session.commit()

    if MasterIngredient.query.count() == 0:

        default_ingredients = [
            MasterIngredient(name="Farina Tipo 0", is_flour=True, is_liquid=False, w_value=240),
            MasterIngredient(name="Farina Tipo 00", is_flour=True, is_liquid=False, w_value=200),
            MasterIngredient(name="Farina Manitoba", is_flour=True, is_liquid=False, w_value=360),
            MasterIngredient(name="Semola Rimacinata", is_flour=True, is_liquid=False, w_value=220),
            MasterIngredient(name="Acqua", is_flour=False, is_liquid=True, w_value=0),
            MasterIngredient(name="Latte Intero", is_flour=False, is_liquid=True, w_value=0),
            MasterIngredient(name="Lievito di Birra Fresco", is_flour=False, is_liquid=False, w_value=0),
            MasterIngredient(name="Lievito di Birra Secco", is_flour=False, is_liquid=False, w_value=0),
            MasterIngredient(name="Sale Marino", is_flour=False, is_liquid=False, w_value=0),
            MasterIngredient(name="Olio EVO", is_flour=False, is_liquid=False, w_value=0),
            MasterIngredient(name="Burro", is_flour=False, is_liquid=False, w_value=0),
            MasterIngredient(name="Zucchero", is_flour=False, is_liquid=False, w_value=0),
            MasterIngredient(name="Malto Diastatico", is_flour=False, is_liquid=False, w_value=0)
        ]

        db.session.bulk_save_objects(default_ingredients)
        db.session.commit()

    setting = Setting.query.first()

    if not setting:
        setting = Setting(
            fresh_to_dry_ratio=3.0,
            tangzhong_flour_percent=5.0,
            tangzhong_liquid_multiplier=5.0,
            site_name="Il Mio Ricettario",
            site_description="Esplora le nostre antiche formule bilanciate professionali. Utilizza i motori di calcolo integrati ad alta precisione per ridimensionare istantaneamente ogni impasto.",
            default_unit="g",
            allow_public_recipes=True,
            theme_active="modern"
        )
        db.session.add(setting)
        db.session.commit()
    else:
        try:
            db.session.execute(db.text("UPDATE settings SET theme_active = 'modern' WHERE theme_active IS NULL"))
            db.session.execute(db.text("UPDATE settings SET site_description = 'Esplora le nostre antiche formule bilanciate professionali. Utilizza i motori di calcolo integrati ad alta precisione per ridimensionare istantaneamente ogni impasto.' WHERE site_description IS NULL"))
            db.session.commit()
        except Exception:
            db.session.rollback()


if __name__ == "__main__":
    app.run(debug=True, port=8080)