from flask import (
    Blueprint,
    render_template
)

from models.recipe import Recipe
from models.ingredient import RecipeIngredient
from models.feature import RecipeFeature
from models.wiki import WikiArticle

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

    feature = RecipeFeature.query.filter_by(
        recipe_id=recipe.id
    ).first()

    return render_template(
        "recipe_public_detail.html",
        recipe=recipe,
        ingredients=ingredients,
        feature=feature
    )


@recipes_bp.route("/wiki")
def wiki_public_list():
    articles = WikiArticle.query.order_by(WikiArticle.category, WikiArticle.id).all()
    categories = {}
    for a in articles:
        categories.setdefault(a.category, []).append(a)
    return render_template(
        "wiki_public.html",
        categories=categories,
        articles=articles
    )


@recipes_bp.route("/wiki/<string:slug>")
def wiki_public_article(slug):
    article = WikiArticle.query.filter_by(slug=slug).first_or_404()
    articles = WikiArticle.query.order_by(WikiArticle.category, WikiArticle.id).all()
    categories = {}
    for a in articles:
        categories.setdefault(a.category, []).append(a)
    return render_template(
        "wiki_public.html",
        categories=categories,
        articles=articles,
        active_article=article
    )