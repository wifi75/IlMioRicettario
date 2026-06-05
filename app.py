from flask import Flask
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


app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)
login_manager.init_app(app)

app.register_blueprint(admin_bp)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


@app.route("/")
def index():
    return "Il Mio Ricettario V1"


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


if __name__ == "__main__":
    app.run(debug=True)