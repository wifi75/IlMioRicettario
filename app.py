from flask import Flask
from flask import redirect
from flask import url_for

from werkzeug.security import generate_password_hash

from config import Config
from extensions import db
from extensions import login_manager

from models.user import User
from models.recipe import Recipe
from models.ingredient import RecipeIngredient
from models.feature import RecipeFeature
from models.setting import Setting
from models.wiki import WikiArticle
from models.parameter import RecipeParameter

from routes.admin import admin_bp
from routes.recipes import recipes_bp


app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)
login_manager.init_app(app)

# Registrazione pulita dei due motori di rotte
app.register_blueprint(recipes_bp)
app.register_blueprint(admin_bp)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(
        User,
        int(user_id)
    )


@app.route("/")
def index():
    # Forza il reindirizzamento alla lista ricette pubblica del frontend
    return redirect(
        url_for("recipes.list_recipes")
    )


with app.app_context():

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