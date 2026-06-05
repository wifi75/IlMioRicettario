from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)

from werkzeug.security import check_password_hash

from extensions import db

from models.user import User
from models.recipe import Recipe
from models.ingredient import RecipeIngredient
from models.feature import RecipeFeature
from models.parameter import RecipeParameter


admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)


@admin_bp.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("admin.dashboard"))

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(
            username=username
        ).first()

        if user and check_password_hash(
            user.password_hash,
            password
        ):
            login_user(user)

            flash(
                "Accesso effettuato correttamente",
                "success"
            )

            return redirect(
                url_for("admin.dashboard")
            )

        flash(
            "Credenziali non valide",
            "danger"
        )

    return render_template(
        "admin/login.html"
    )


@admin_bp.route("/logout")
@login_required
def logout():

    logout_user()

    flash(
        "Logout effettuato",
        "info"
    )

    return redirect(
        url_for("admin.login")
    )


@admin_bp.route("/dashboard")
@login_required
def dashboard():

    recipes_count = Recipe.query.count()

    return render_template(
        "admin/dashboard.html",
        recipes_count=recipes_count
    )


@admin_bp.route("/recipes")
@login_required
def recipes():

    recipes = Recipe.query.order_by(
        Recipe.id.desc()
    ).all()

    return render_template(
        "admin/recipes.html",
        recipes=recipes
    )


@admin_bp.route(
    "/recipes/new",
    methods=["GET", "POST"]
)
@login_required
def recipe_new():

    if request.method == "POST":

        recipe = Recipe(
            name=request.form["name"],
            slug=request.form["slug"],
            description=request.form["description"],
            instructions=request.form["instructions"]
        )

        db.session.add(recipe)
        db.session.commit()

        feature = RecipeFeature(
            recipe_id=recipe.id
        )

        db.session.add(feature)
        db.session.commit()

        flash(
            "Ricetta creata correttamente",
            "success"
        )

        return redirect(
            url_for("admin.recipes")
        )

    return render_template(
        "admin/recipe_form.html"
    )


@admin_bp.route("/recipe/<int:id>")
@login_required
def recipe_detail(id):

    recipe = Recipe.query.get_or_404(id)

    ingredients = RecipeIngredient.query.filter_by(
        recipe_id=recipe.id
    ).order_by(
        RecipeIngredient.sort_order
    ).all()

    feature = RecipeFeature.query.filter_by(
        recipe_id=recipe.id
    ).first()

    parameters = RecipeParameter.query.filter_by(
        recipe_id=recipe.id
    ).order_by(
        RecipeParameter.sort_order
    ).all()

    return render_template(
        "admin/recipe_detail.html",
        recipe=recipe,
        ingredients=ingredients,
        feature=feature,
        parameters=parameters
    )


@admin_bp.route(
    "/recipe/<int:id>/ingredient/new",
    methods=["POST"]
)
@login_required
def ingredient_new(id):

    recipe = Recipe.query.get_or_404(id)

    ingredient = RecipeIngredient(
        recipe_id=recipe.id,
        name=request.form["name"],
        quantity=float(request.form["quantity"]),
        unit=request.form["unit"],
        is_flour="is_flour" in request.form,
        is_liquid="is_liquid" in request.form
    )

    db.session.add(ingredient)
    db.session.commit()

    flash(
        "Ingrediente aggiunto",
        "success"
    )

    return redirect(
        url_for(
            "admin.recipe_detail",
            id=recipe.id
        )
    )


@admin_bp.route("/ingredient/delete/<int:id>")
@login_required
def ingredient_delete(id):

    ingredient = RecipeIngredient.query.get_or_404(id)

    recipe_id = ingredient.recipe_id

    db.session.delete(ingredient)
    db.session.commit()

    flash(
        "Ingrediente eliminato",
        "warning"
    )

    return redirect(
        url_for(
            "admin.recipe_detail",
            id=recipe_id
        )
    )


@admin_bp.route("/recipes/delete/<int:id>")
@login_required
def recipe_delete(id):

    recipe = Recipe.query.get_or_404(id)

    db.session.delete(recipe)
    db.session.commit()

    flash(
        "Ricetta eliminata",
        "warning"
    )

    return redirect(
        url_for("admin.recipes")
    )