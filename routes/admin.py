import os
import base64
from datetime import datetime
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    jsonify
)

from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)

from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from extensions import db

from models.user import User
from models.recipe import Recipe
from models.ingredient import RecipeIngredient
from models.feature import RecipeFeature
from models.parameter import RecipeParameter
from models.setting import Setting
from models.wiki import WikiArticle
from models.ingredient_master import MasterIngredient
from models.bakery_pan import MasterBakeryPan


admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)

# =========================================================================
# 📸 CONFIGURAZIONE MULTIMEDIALE AVANZATA (CON EDITOR DI RITAGLIO INTEGRATO)
# =========================================================================
UPLOAD_FOLDER = os.path.join('static', 'uploads', 'recipes')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def handle_image_assignment(recipe_slug):
    """Gestore unico professionale che riceve e decodifica l'immagine ritagliata dall'editor"""
    
    # 1. Intercettamento immediato dello scollegamento da interfaccia (Tasto X)
    if request.form.get("clear_current_image_flag") == "true":
        return None

    # 2. Controllo se arriva un'immagine ritagliata via JavaScript (Stringa Base64)
    cropped_base64 = request.form.get("cropped_image_base64", "").strip()
    if cropped_base64 and "," in cropped_base64:
        try:
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            # Separiamo l'intestazione MIME-type dai dati binari reali criptati della foto
            header, base64_data = cropped_base64.split(",", 1)
            image_binary_data = base64.b64decode(base64_data)
            
            # Salviamo il ritaglio controllato in formato nativo .png stabile ad alta definizione
            filename = f"recipe_{recipe_slug}_{int(datetime.utcnow().timestamp())}.png"
            secure_name = secure_filename(filename)
            file_path = os.path.join(UPLOAD_FOLDER, secure_name)
            
            with open(file_path, "wb") as f:
                f.write(image_binary_data)
                
            return secure_name
        except Exception as e:
            print(f"[-] Errore critico durante la decodifica del ritaglio foto: {e}")

    # 3. Se non c'è un ritaglio fresco, controlla se l'utente ha scelto una foto esistente dalla galleria
    selected_existing = request.form.get("selected_existing_image", "").strip()
    if selected_existing:
        return selected_existing

    # Ritorna questo flag speciale se l'utente non ha apportato modifiche al reparto multimediale
    return "__KEEP_OLD__"


@admin_bp.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("admin.recipes"))

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
                url_for("admin.recipes")
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
    return redirect(url_for("admin.recipes"))


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

        instructions_text = request.form.get("instructions", "").strip()
        preferment_text = request.form.get("preferment_instructions", "").strip()
        badge_text_input = request.form.get("badge_text", "Antica Formula Bilanciata").strip()
        recipe_slug = request.form["slug"].strip()

        # Intercettamento multimediale
        image_name = handle_image_assignment(recipe_slug)
        if image_name == "__KEEP_OLD__":
            image_name = None

        try:
            fresco_raw = request.form.get("yeast_fresh_val", "3.0").replace(",", ".")
            secco_raw = request.form.get("yeast_dry_val", "1.0").replace(",", ".")
            
            fresco_val = float(fresco_raw) if fresco_raw else 3.0
            secco_val = float(secco_raw) if secco_raw else 1.0
            yeast_ratio_val = round(fresco_val / secco_val, 1) if secco_val > 0 else 3.0
        except (ValueError, TypeError):
            fresco_val = 3.0
            secco_val = 1.0
            yeast_ratio_val = 3.0

        recipe = Recipe(
            name=request.form["name"],
            slug=recipe_slug,
            badge_text=badge_text_input if badge_text_input else "Antica Formula Bilanciata",
            description=request.form.get("description", "").strip(),
            instructions=instructions_text,
            is_published="is_published" in request.form,
            image=image_name,
            
            temp_chiusura=float(request.form.get("temp_chiusura", 24.0)) if request.form.get("temp_chiusura") else 24.0,
            tempo_autolisi=int(request.form.get("tempo_autolisi", 0)) if request.form.get("tempo_autolisi") else 0,
            tempo_puntata=int(request.form.get("tempo_puntata", 0)) if request.form.get("tempo_puntata") else 0,
            tempo_appretto=int(request.form.get("tempo_appretto", 0)) if request.form.get("tempo_appretto") else 0,
            
            show_chiusura="show_chiusura" in request.form,
            show_autolysis="show_autolysis" in request.form,
            show_puntata="show_puntata" in request.form,
            puntata_fino_al_raddoppio="puntata_fino_al_raddoppio" in request.form,
            show_appretto="show_appretto" in request.form,
            
            fermentation_type=request.form.get("fermentation_type", "diretto"),
            preferment_instructions=preferment_text,
            
            yeast_ratio=yeast_ratio_val,
            yeast_fresh_saved=fresco_val,
            yeast_dry_saved=secco_val
        )

        selected_pan_ids = request.form.getlist("pans[]")
        for pan_id in selected_pan_ids:
            pan = MasterBakeryPan.query.get(int(pan_id))
            if pan:
                recipe.pans.append(pan)

        db.session.add(recipe)
        db.session.commit()

        feature = RecipeFeature(
            recipe_id=recipe.id,
            enable_piece_count="enable_piece_count" in request.form,
            enable_piece_weight="enable_piece_weight" in request.form,
            enable_yeast_type="enable_yeast_type" in request.form,
            enable_tangzhong="enable_tangzhong" in request.form,
            enable_poolish=recipe.fermentation_type == "poolish",
            enable_biga=recipe.fermentation_type == "biga"
        )
        db.session.add(feature)

        ing_names = request.form.getlist("ing_name[]")
        ing_qtys = request.form.getlist("ing_qty[]")
        ing_units = request.form.getlist("ing_unit[]")
        ing_ws = request.form.getlist("ing_w[]")

        for i in range(len(ing_names)):
            if not ing_names[i].strip():
                continue

            is_flour_checked = request.form.get(f"ing_is_flour_{i}") == "true"
            is_liquid_checked = request.form.get(f"ing_is_liquid_{i}") == "true"
            current_w = int(ing_ws[i]) if (i < len(ing_ws) and ing_ws[i]) else 0

            ingredient = RecipeIngredient(
                recipe_id=recipe.id,
                name=ing_names[i],
                quantity=float(ing_qtys[i]) if ing_qtys[i] else 0.0,
                unit=ing_units[i],
                is_flour=is_flour_checked,
                is_liquid=is_liquid_checked,
                w_value=current_w,
                sort_order=i
            )
            db.session.add(ingredient)

        db.session.commit()

        flash("Formula bilanciata e salvata con successo!", "success")
        return redirect(url_for("admin.recipes"))

    master_ingredients = MasterIngredient.query.order_by(MasterIngredient.name).all()
    master_pans = MasterBakeryPan.query.order_by(MasterBakeryPan.name).all()
    
    return render_template(
        "admin/recipe_form.html",
        master_ingredients_list=master_ingredients,
        master_pans_list=master_pans,
        computed_fresh_val=3.0,
        computed_dry_val=1.0
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
    """CABINA DI REGIA: Gestione strutturale completa della formula"""
    recipe = Recipe.query.get_or_404(id)

    feature = RecipeFeature.query.filter_by(
        recipe_id=recipe.id
    ).first()

    if not feature:
        feature = RecipeFeature(recipe_id=recipe.id)
        db.session.add(feature)
        db.session.commit()

    if request.method == "POST":

        instructions_text = request.form.get("instructions", "").strip()
        preferment_text = request.form.get("preferment_instructions", "").strip()
        badge_text_input = request.form.get("badge_text", "Antica Formula Bilanciata").strip()
        recipe_slug = request.form["slug"].strip()

        # Intercettamento immagine e controllo del mantenimento o della pulizia
        new_image = handle_image_assignment(recipe_slug)
        if new_image is None:
            recipe.image = None  # Ricevuto comando clear del legame
        elif new_image != "__KEEP_OLD__":
            recipe.image = new_image  # Caricato nuovo file o scelta da libreria

        try:
            fresco_raw = request.form.get("yeast_fresh_val", "3.0").replace(",", ".")
            secco_raw = request.form.get("yeast_dry_val", "1.0").replace(",", ".")
            
            fresco_val = float(fresco_raw) if fresco_raw else 3.0
            secco_val = float(secco_raw) if secco_raw else 1.0
            
            yeast_ratio_val = round(fresco_val / secco_val, 1) if secco_val > 0 else 3.0
        except (ValueError, TypeError):
            fresco_val = 3.0
            secco_val = 1.0
            yeast_ratio_val = 3.0

        recipe.name = request.form["name"]
        recipe.slug = recipe_slug
        recipe.icon = request.form.get("icon", "bi-journal-text")
        recipe.badge_text = badge_text_input if badge_text_input else "Antica Formula Bilanciata"
        recipe.description = request.form.get("description", "").strip()
        recipe.instructions = instructions_text
        recipe.is_published = "is_published" in request.form
        
        recipe.yeast_ratio = yeast_ratio_val
        recipe.yeast_fresh_saved = fresco_val
        recipe.yeast_dry_saved = secco_val

        recipe.temp_chiusura = float(request.form.get("temp_chiusura", 24.0)) if request.form.get("temp_chiusura") else 24.0
        recipe.tempo_autolisi = int(request.form.get("tempo_autolisi", 0)) if request.form.get("tempo_autolisi") else 0
        recipe.tempo_puntata = int(request.form.get("tempo_puntata", 0)) if request.form.get("tempo_puntata") else 0
        recipe.tempo_appretto = int(request.form.get("tempo_appretto", 0)) if request.form.get("tempo_appretto") else 0

        recipe.show_chiusura = "show_chiusura" in request.form
        recipe.show_autolysis = "show_autolysis" in request.form
        recipe.show_puntata = "show_puntata" in request.form
        recipe.puntata_fino_al_raddoppio = "puntata_fino_al_raddoppio" in request.form
        recipe.show_appretto = "show_appretto" in request.form

        recipe.fermentation_type = request.form.get("fermentation_type", "diretto")
        recipe.preferment_instructions = preferment_text

        feature.enable_piece_count = "enable_piece_count" in request.form
        feature.enable_piece_weight = "enable_piece_weight" in request.form
        feature.enable_yeast_type = "enable_yeast_type" in request.form
        feature.enable_tangzhong = "enable_tangzhong" in request.form
        feature.enable_poolish = recipe.fermentation_type == "poolish"
        feature.enable_biga = recipe.fermentation_type == "biga"

        recipe.pans.clear()
        selected_pan_ids = request.form.getlist("pans[]")
        for pan_id in selected_pan_ids:
            pan = MasterBakeryPan.query.get(int(pan_id))
            if pan:
                recipe.pans.append(pan)

        RecipeIngredient.query.filter_by(recipe_id=recipe.id).delete()

        ing_names = request.form.getlist("ing_name[]")
        ing_qtys = request.form.getlist("ing_qty[]")
        ing_units = request.form.getlist("ing_unit[]")
        ing_ws = request.form.getlist("ing_w[]")

        for i in range(len(ing_names)):
            if not ing_names[i].strip():
                continue

            is_flour_checked = request.form.get(f"ing_is_flour_{i}") == "true"
            is_liquid_checked = request.form.get(f"ing_is_liquid_{i}") == "true"
            current_w = int(ing_ws[i]) if (i < len(ing_ws) and ing_ws[i]) else 0

            ingredient = RecipeIngredient(
                recipe_id=recipe.id,
                name=ing_names[i],
                quantity=float(ing_qtys[i]) if ing_qtys[i] else 0.0,
                unit=ing_units[i],
                is_flour=is_flour_checked,
                is_liquid=is_liquid_checked,
                w_value=current_w,
                sort_order=i
            )
            db.session.add(ingredient)

        db.session.commit()

        flash("Ricetta aggiornata e ribilanciata correttamente", "success")
        return redirect(url_for("admin.recipes"))

    ingredients = RecipeIngredient.query.filter_by(
        recipe_id=recipe.id
    ).order_by(
        RecipeIngredient.sort_order
    ).all()

    master_ingredients = MasterIngredient.query.order_by(MasterIngredient.name).all()
    master_pans = MasterBakeryPan.query.order_by(MasterBakeryPan.name).all()

    f_val = recipe.yeast_fresh_saved if recipe.yeast_fresh_saved is not None else (recipe.yeast_ratio if recipe.yeast_ratio else 3.0)
    d_val = recipe.yeast_dry_saved if recipe.yeast_dry_saved is not None else 1.0

    return render_template(
        "admin/recipe_form.html",
        recipe=recipe,
        feature=feature,
        ingredients=ingredients,
        master_ingredients_list=master_ingredients,
        master_pans_list=master_pans,
        computed_fresh_val=f_val,  
        computed_dry_val=d_val     
    )


# ==========================================================
# SEZIONE API MULTIMEDIALE: GALLERIA FOTO (PNG/JPG ACCETTATI)
# ==========================================================

@admin_bp.route("/api/images/list", methods=["GET"])
@login_required
def api_images_list():
    """Restituisce l'elenco di tutte le immagini caricate precedentemente sul server"""
    if not os.path.exists(UPLOAD_FOLDER):
        return jsonify([])
    files = [f for f in os.listdir(UPLOAD_FOLDER) if os.path.isfile(os.path.join(UPLOAD_FOLDER, f)) and f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    return jsonify(files)


@admin_bp.route("/api/images/delete/<string:filename>", methods=["POST"])
@login_required
def api_image_delete(filename):
    """Elimina definitivamente un file multimediale dal server"""
    secure_name = secure_filename(filename)
    file_path = os.path.join(UPLOAD_FOLDER, secure_name)
    
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            recipes_using_it = Recipe.query.filter_by(image=secure_name).all()
            for r in recipes_using_it:
                r.image = None
            db.session.commit()
            return jsonify({"success": True, "message": "Immagine eliminata fisicamente dal server"})
        except Exception as e:
            return jsonify({"success": False, "message": str(e)}), 500
            
    return jsonify({"success": False, "message": "File non trovato"}), 404


# ==========================================================
# SEZIONE: ANAGRAFICA INFINITA DELLE TEGLIE / STAMPI MASTER
# ==========================================================

@admin_bp.route("/pans/master", methods=["GET"])
@login_required
def master_pans_view():
    master_pans = MasterBakeryPan.query.order_by(MasterBakeryPan.name).all()
    return render_template(
        "admin/pans_master.html",
        master_pans_list=master_pans
    )


@admin_bp.route("/pans/master/add", methods=["POST"])
@login_required
def master_pan_add():
    name = request.form.get("name", "").strip()
    pan_type = request.form.get("pan_type", "rettangolare")
    weight_capacity = request.form.get("weight_capacity", 0.0)

    if name:
        existing = MasterBakeryPan.query.filter_by(name=name).first()
        if not existing:
            try:
                new_pan = MasterBakeryPan(
                    name=name,
                    pan_type=pan_type,
                    weight_capacity=float(weight_capacity) if weight_capacity else 0.0
                )
                db.session.add(new_pan)
                db.session.commit()
                flash(f"Teglia '{name}' aggiunta alla tua flotta globale!", "success")
            except ValueError:
                flash("Errore: Inserisci un peso di capacità valido", "danger")
        else:
            flash("Questa tipologia di teglia esiste già nel database", "warning")
    return redirect(url_for("admin.master_pans_view"))


@admin_bp.route("/pans/master/delete/<int:id>", methods=["GET"])
@login_required
def master_pan_delete(id):
    pan = MasterBakeryPan.query.get_or_404(id)
    name = pan.name
    db.session.delete(pan)
    db.session.commit()
    flash(f"Teglia '{name}' rimossa dalla configurazione", "warning")
    return redirect(url_for("admin.master_pans_view"))


# ==========================================================
# SEZIONE WIKI & ARTICOLI
# ==========================================================

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


# ==========================================================
# SEZIONE INGREDIENTI MASTER & IMPOSTAZIONI GLOBALI
# ==========================================================

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


@admin_bp.route("/settings/theme", methods=["GET", "POST"])
@login_required
def settings_theme():
    try:
        db.session.execute(db.text("ALTER TABLE settings ADD COLUMN theme_active VARCHAR(50) DEFAULT 'modern'"))
        db.session.commit()
    except Exception:
        db.session.rollback()

    try:
        db.session.execute(db.text("ALTER TABLE settings ADD COLUMN site_description TEXT"))
        db.session.commit()
    except Exception:
        db.session.rollback()

    setting = Setting.query.first()
    if not setting:
        setting = Setting(fresh_to_dry_ratio=3.0, theme_active="modern")
        db.session.add(setting)
        db.session.commit()

    if request.method == "POST":
        selected_theme = request.form.get("theme_active", "modern").strip()
        new_site_name = request.form.get("site_name", "").strip()
        new_site_description = request.form.get("site_description", "").strip()
        
        db.session.execute(
            db.text("UPDATE settings SET theme_active = :theme, site_name = :name, site_description = :desc"),
            {"theme": selected_theme, "name": new_site_name, "desc": new_site_description}
        )
        db.session.commit()

        flash("Configurazione, look estetico e testi della Home salvati con successo!", "success")
        return redirect(url_for("admin.settings_theme"))

    setting = Setting.query.first()
    return render_template("admin/settings_theme.html", setting=setting)


@admin_bp.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "POST":
        old_password = request.form.get("old_password")
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")

        if not check_password_hash(current_user.password_hash, old_password):
            flash("La password attuale inserita non è corretta.", "danger")
            return redirect(url_for("admin.change_password"))

        if new_password != confirm_password:
            flash("La nuova password e la password di conferma non coincidono.", "danger")
            return redirect(url_for("admin.change_password"))

        if len(new_password) < 6:
            flash("La nuova password deve contenere almeno 6 caratteri.", "warning")
            return redirect(url_for("admin.change_password"))

        current_user.password_hash = generate_password_hash(new_password)
        db.session.commit()

        flash("Password amministratore aggiornata con successo!", "success")
        return redirect(url_for("admin.recipes"))

    return render_template("admin/change_password.html")