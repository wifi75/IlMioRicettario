from flask import (
    Blueprint,
    render_template
)

from models.recipe import Recipe
from models.ingredient import RecipeIngredient
from models.setting import Setting
from models.feature import RecipeFeature  # <-- AGGIUNTO L'IMPORT DELLA FEATURE!


recipes_bp = Blueprint(
    "recipes",
    __name__
)


@recipes_bp.route("/")
def list_recipes():

    recipes = Recipe.query.order_by(
        Recipe.name
    ).all()

    return render_template(
        "recipes_list.html",
        recipes=recipes
    )


@recipes_bp.route("/recipe/<string:slug>")
def public_detail(slug):

    recipe = Recipe.query.filter_by(
        slug=slug
    ).first_or_404()

    ingredients = RecipeIngredient.query.filter_by(
        recipe_id=recipe.id
    ).all()

    settings_data = Setting.query.first()

    # AGGIUNTO: Carichiamo la feature specifica di questa ricetta
    feature = RecipeFeature.query.filter_by(
        recipe_id=recipe.id
    ).first()

    return render_template(
        "recipe_public_detail.html",
        recipe=recipe,
        ingredients=ingredients,
        settings_data=settings_data,
        feature=feature  # <-- PASSIAMO LA FEATURE AL TEMPLATE PUBBLICO!
    )