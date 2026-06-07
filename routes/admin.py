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
from models.setting import Setting
from models.wiki import WikiArticle
from models.ingredient_master import MasterIngredient


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
    wiki_count = WikiArticle.query.count()

    return render_template(
        "admin/dashboard.html",
        recipes_count=recipes_count,
        wiki_count=wiki_count
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
            instructions=request.form["instructions"],
            is_published="is_published" in request.form,
            temp_chiusura=float(request.form.get("temp_chiusura", 24.0)) if request.form.get("temp_chiusura") else 24.0,
            tempo_autolisi=int(request.form.get("tempo_autolisi", 0)) if request.form.get("tempo_autolisi") else 0,
            tempo_puntata=int(request.form.get("tempo_puntata", 0)) if request.form.get("tempo_puntata") else 0,
            tempo_appretto=int(request.form.get("tempo_appretto", 0)) if request.form.get("tempo_appretto") else 0
        )

        db.session.add(recipe)
        db.session.commit()

        pref_type = request.form.get("preferment_type", "none")

        feature = RecipeFeature(
            recipe_id=recipe.id,
            enable_piece_count="enable_piece_count" in request.form,
            enable_piece_weight="enable_piece_weight" in request.form,
            enable_yeast_type="enable_yeast_type" in request.form,
            enable_tangzhong="enable_tangzhong" in request.form,
            enable_poolish=pref_type == "poolish",
            enable_biga=pref_type == "biga"
        )

        db.session.add(feature)

        ing_names = request.form.getlist("ing_name[]")
        ing_qtys = request.form.getlist("ing_qty[]")
        ing_units = request.form.getlist("ing_unit[]")

        for i in range(len(ing_names)):
            if not ing_names[i].strip():
                continue

            is_flour_checked = request.form.get(f"ing_is_flour_{i}") == "true"
            is_liquid_checked = request.form.get(f"ing_is_liquid_{i}") == "true"

            ingredient = RecipeIngredient(
                recipe_id=recipe.id,
                name=ing_names[i],
                quantity=float(ing_qtys[i]) if ing_qtys[i] else 0.0,
                unit=ing_units[i],
                is_flour=is_flour_checked,
                is_liquid=is_liquid_checked,
                sort_order=i
            )
            db.session.add(ingredient)

        db.session.commit()

        flash(
            "Formula bilanciata e salvata con successo!",
            "success"
        )

        return redirect(
            url_for("admin.recipes")
        )

    master_ingredients = MasterIngredient.query.order_by(MasterIngredient.name).all()
    return render_template(
        "admin/recipe_form.html",
        master_ingredients_list=master_ingredients
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


@admin_bp.route(
    "/recipe/edit/<int:id>",
    methods=["GET", "POST"]
)
@login_required
def recipe_edit(id):

    recipe = Recipe.query.get_or_404(id)

    feature = RecipeFeature.query.filter_by(
        recipe_id=recipe.id
    ).first()

    if not feature:
        feature = RecipeFeature(recipe_id=recipe.id)
        db.session.add(feature)
        db.session.commit()

    if request.method == "POST":

        recipe.name = request.form["name"]
        recipe.slug = request.form["slug"]
        recipe.description = request.form["description"]
        recipe.instructions = request.form["instructions"]
        recipe.is_published = "is_published" in request.form

        recipe.temp_chiusura = float(request.form.get("temp_chiusura", 24.0)) if request.form.get("temp_chiusura") else 24.0
        recipe.tempo_autolisi = int(request.form.get("tempo_autolisi", 0)) if request.form.get("tempo_autolisi") else 0
        recipe.tempo_puntata = int(request.form.get("tempo_puntata", 0)) if request.form.get("tempo_puntata") else 0
        recipe.tempo_appretto = int(request.form.get("tempo_appretto", 0)) if request.form.get("tempo_appretto") else 0

        pref_type = request.form.get("preferment_type", "none")

        feature.enable_piece_count = "enable_piece_count" in request.form
        feature.enable_piece_weight = "enable_piece_weight" in request.form
        feature.enable_yeast_type = "enable_yeast_type" in request.form
        feature.enable_tangzhong = "enable_tangzhong" in request.form
        feature.enable_poolish = pref_type == "poolish"
        feature.enable_biga = pref_type == "biga"

        RecipeIngredient.query.filter_by(recipe_id=recipe.id).delete()

        ing_names = request.form.getlist("ing_name[]")
        ing_qtys = request.form.getlist("ing_qty[]")
        ing_units = request.form.getlist("ing_unit[]")

        for i in range(len(ing_names)):
            if not ing_names[i].strip():
                continue

            is_flour_checked = request.form.get(f"ing_is_flour_{i}") == "true"
            is_liquid_checked = request.form.get(f"ing_is_liquid_{i}") == "true"

            ingredient = RecipeIngredient(
                recipe_id=recipe.id,
                name=ing_names[i],
                quantity=float(ing_qtys[i]) if ing_qtys[i] else 0.0,
                unit=ing_units[i],
                is_flour=is_flour_checked,
                is_liquid=is_liquid_checked,
                sort_order=i
            )
            db.session.add(ingredient)

        db.session.commit()

        flash(
            "Ricetta aggiornata e ribilanciata correttamente",
            "success"
        )

        return redirect(
            url_for("admin.recipes")
        )

    ingredients = RecipeIngredient.query.filter_by(
        recipe_id=recipe.id
    ).order_by(
        RecipeIngredient.sort_order
    ).all()

    master_ingredients = MasterIngredient.query.order_by(MasterIngredient.name).all()

    return render_template(
        "admin/recipe_edit_form.html",
        recipe=recipe,
        feature=feature,
        ingredients=ingredients,
        master_ingredients_list=master_ingredients
    )


@admin_bp.route("/wiki")
@login_required
def wiki_list():

    articles = WikiArticle.query.order_by(
        WikiArticle.title
    ).all()

    return render_template(
        "admin/wiki_list.html",
        articles=articles
    )


@admin_bp.route(
    "/wiki/new",
    methods=["GET", "POST"]
)
@login_required
def wiki_new():

    if request.method == "POST":

        article = WikiArticle(
            title=request.form["title"],
            slug=request.form["slug"],
            content=request.form["content"],
            category=request.form.get("category", "Generale")
        )

        db.session.add(article)
        db.session.commit()

        flash(
            "Articolo della Wiki creato",
            "success"
        )

        return redirect(
            url_for("admin.wiki_list")
        )

    return render_template(
        "admin/wiki_form.html"
    )


@admin_bp.route("/wiki/delete/<int:id>")
@login_required
def wiki_delete(id):

    article = WikiArticle.query.get_or_404(id)

    db.session.delete(article)
    db.session.commit()

    flash(
        "Articolo eliminato dalla Wiki",
        "warning"
    )

    return redirect(
        url_for("admin.wiki_list")
    )


@admin_bp.route("/ingredients/master", methods=["GET"])
@login_required
def master_ingredients_view():
    master_ingredients = MasterIngredient.query.order_by(MasterIngredient.name).all()
    return render_template(
        "admin/ingredients_master.html",
        master_ingredients_list=master_ingredients
    )


@admin_bp.route("/ingredients/master/add", methods=["POST"])
@login_required
def master_ingredient_add():
    name = request.form.get("name", "").strip()
    if name:
        existing = MasterIngredient.query.filter_by(name=name).first()
        if not existing:
            new_ing = MasterIngredient(
                name=name,
                is_flour="is_flour" in request.form,
                is_liquid="is_liquid" in request.form
            )
            db.session.add(new_ing)
            db.session.commit()
            flash(f"'{name}' aggiunto all'anagrafica di base!", "success")
        else:
            flash("Questo ingrediente esiste già nel database", "warning")
    return redirect(url_for("admin.master_ingredients_view"))


@admin_bp.route("/ingredients/master/delete/<int:id>", methods=["GET"])
@login_required
def master_ingredient_delete(id):
    ing = MasterIngredient.query.get_or_404(id)
    name = ing.name
    db.session.delete(ing)
    db.session.commit()
    flash(f"'{name}' rimosso dall'anagrafica del database", "warning")
    return redirect(url_for("admin.master_ingredients_view"))


@admin_bp.route("/settings/yeast", methods=["GET", "POST"])
@login_required
def settings_yeast():

    setting = Setting.query.first()

    if request.method == "POST":

        try:

            ratio_value = float(request.form.get("fresh_to_dry_ratio", 3.0))
            setting.fresh_to_dry_ratio = ratio_value
            db.session.commit()

            flash(
                "Coefficiente di conversione lieviti aggiornato correttamente!",
                "success"
            )

        except ValueError:

            flash(
                "Errore: Inserisci un valore numerico valido (es. 3.0)",
                "danger"
            )

        return redirect(
            url_for("admin.settings_yeast")
        )

    return render_template(
        "admin/settings_yeast.html",
        setting=setting
    )