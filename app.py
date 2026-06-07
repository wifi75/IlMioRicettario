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

from routes.recipes import recipes_bp
# BLINDATO: Forza il caricamento del Blueprint corretto per evitare conflitti di sotto-cartelle
from routes.admin import admin_bp


app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)
login_manager.init_app(app)

# INIZIALIZZAZIONE DEL MOTORE DI MIGRAZIONE DEL DATABASE
migrate = Migrate(app, db)

# Registrazione dei motori di rotte
app.register_blueprint(recipes_bp)
app.register_blueprint(admin_bp)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(
        User,
        int(user_id)
    )


# PROCESSORE DI CONTESTO GLOBALE PULITO
@app.context_processor
def inject_global_settings():
    return dict(
        settings_data=Setting.query.first()
    )


@app.route("/")
def index():
    return redirect(
        url_for("recipes.list_recipes")
    )


with app.app_context():

    # NOTA: create_all() rimane attivo solo come salvagente per installazioni da zero
    db.create_all()

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

    # Iniezione record di partenza nell'anagrafica centralizzata comprensiva di parametri W
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
        print("Anagrafica ingredienti master pre-popolata con successo con valori W!")

    setting = Setting.query.first()

    if not setting:

        setting = Setting(
            fresh_to_dry_ratio=3.0,
            tangzhong_flour_percent=5.0,
            tangzhong_liquid_multiplier=5.0,
            site_name="Il Mio Ricettario",
            default_unit="g",
            allow_public_recipes=True
        )

        db.session.add(setting)
        db.session.commit()


if __name__ == "__main__":
    app.run(debug=True, port=8080)