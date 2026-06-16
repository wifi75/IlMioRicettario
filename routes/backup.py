import io
import json
import os
import zipfile
from datetime import datetime

from flask import (
    Blueprint, flash, jsonify, redirect, render_template,
    request, send_file, url_for
)
from flask_login import login_required

from extensions import db
from models.bakery_pan import MasterBakeryPan
from models.feature import RecipeFeature
from models.ingredient import RecipeIngredient
from models.ingredient_master import MasterIngredient
from models.recipe import Recipe
from models.setting import Setting
from models.wiki import WikiArticle

backup_bp = Blueprint('backup', __name__, url_prefix='/admin/backup')

BACKUP_VERSION = '3.0'
UPLOAD_FOLDER = os.path.join('static', 'uploads', 'recipes')


# ─────────────────────────────────────────────
# Helpers di serializzazione
# ─────────────────────────────────────────────

def _serialize_recipe(r):
    return {
        'name': r.name,
        'slug': r.slug,
        'badge_text': r.badge_text,
        'description': r.description,
        'instructions': r.instructions,
        'icon': r.icon,
        'is_published': r.is_published,
        'temp_chiusura': r.temp_chiusura,
        'tempo_autolisi': r.tempo_autolisi,
        'tempo_puntata': r.tempo_puntata,
        'tempo_appretto': r.tempo_appretto,
        'show_chiusura': r.show_chiusura,
        'show_autolysis': r.show_autolysis,
        'show_puntata': r.show_puntata,
        'puntata_fino_al_raddoppio': r.puntata_fino_al_raddoppio,
        'show_appretto': r.show_appretto,
        'fermentation_type': r.fermentation_type,
        'preferment_instructions': r.preferment_instructions,
        'yeast_ratio': r.yeast_ratio,
        'yeast_fresh_saved': r.yeast_fresh_saved,
        'yeast_dry_saved': r.yeast_dry_saved,
        'pans': [p.name for p in r.pans],
        'ingredients': [
            {
                'name': ing.name,
                'quantity': ing.quantity,
                'percentage': ing.percentage,
                'unit': ing.unit,
                'is_flour': ing.is_flour,
                'is_liquid': ing.is_liquid,
                'w_value': ing.w_value,
                'is_optional': ing.is_optional,
                'sort_order': ing.sort_order,
                'notes': ing.notes,
            }
            for ing in r.ingredients
        ],
        'features': _serialize_features(r.features[0] if r.features else None),
    }


def _serialize_features(f):
    if not f:
        return {}
    return {
        'enable_piece_count': f.enable_piece_count,
        'enable_piece_weight': f.enable_piece_weight,
        'enable_pans': f.enable_pans,
        'enable_hydration': f.enable_hydration,
        'enable_yeast_type': f.enable_yeast_type,
        'enable_tangzhong': f.enable_tangzhong,
        'enable_poolish': f.enable_poolish,
        'enable_biga': f.enable_biga,
        'enable_sourdough': f.enable_sourdough,
        'enable_baker_percentage': f.enable_baker_percentage,
    }


def _recipes_payload():
    return {
        'version': BACKUP_VERSION,
        'type': 'recipes',
        'exported_at': datetime.utcnow().isoformat(),
        'recipes': [_serialize_recipe(r) for r in Recipe.query.order_by(Recipe.id).all()],
    }


def _config_payload():
    s = Setting.query.first()
    return {
        'version': BACKUP_VERSION,
        'type': 'config',
        'exported_at': datetime.utcnow().isoformat(),
        'settings': {
            'fresh_to_dry_ratio': s.fresh_to_dry_ratio if s else 3.0,
            'tangzhong_flour_percent': s.tangzhong_flour_percent if s else 5.0,
            'tangzhong_liquid_multiplier': s.tangzhong_liquid_multiplier if s else 5.0,
            'site_name': s.site_name if s else '',
            'site_description': s.site_description if s else '',
            'default_unit': s.default_unit if s else 'g',
            'allow_public_recipes': s.allow_public_recipes if s else True,
            'theme_active': s.theme_active if s else 'modern',
        },
        'master_ingredients': [
            {'name': i.name, 'is_flour': i.is_flour, 'is_liquid': i.is_liquid, 'w_value': i.w_value}
            for i in MasterIngredient.query.order_by(MasterIngredient.name).all()
        ],
        'master_pans': [
            {'name': p.name, 'pan_type': p.pan_type, 'weight_capacity': p.weight_capacity}
            for p in MasterBakeryPan.query.order_by(MasterBakeryPan.name).all()
        ],
        'wiki_articles': [
            {'title': a.title, 'slug': a.slug, 'content': a.content, 'category': a.category}
            for a in WikiArticle.query.order_by(WikiArticle.id).all()
        ],
    }


def _json_bytes(data):
    return json.dumps(data, ensure_ascii=False, indent=2).encode('utf-8')


def _ts():
    return datetime.now().strftime('%Y%m%d_%H%M')


# ─────────────────────────────────────────────
# Route: pagina backup
# ─────────────────────────────────────────────

@backup_bp.route('/')
@login_required
def backup_page():
    recipe_count = Recipe.query.count()
    ingredient_count = MasterIngredient.query.count()
    pan_count = MasterBakeryPan.query.count()
    wiki_count = WikiArticle.query.count()
    return render_template('admin/backup.html',
        recipe_count=recipe_count,
        ingredient_count=ingredient_count,
        pan_count=pan_count,
        wiki_count=wiki_count,
    )


# ─────────────────────────────────────────────
# Export
# ─────────────────────────────────────────────

@backup_bp.route('/export/recipes')
@login_required
def export_recipes():
    data = _recipes_payload()
    buf = io.BytesIO(_json_bytes(data))
    buf.seek(0)
    return send_file(buf, mimetype='application/json', as_attachment=True,
                     download_name=f'ricette_{_ts()}.json')


@backup_bp.route('/export/config')
@login_required
def export_config():
    data = _config_payload()
    buf = io.BytesIO(_json_bytes(data))
    buf.seek(0)
    return send_file(buf, mimetype='application/json', as_attachment=True,
                     download_name=f'configurazione_{_ts()}.json')


@backup_bp.route('/export/full')
@login_required
def export_full():
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(f'ricette_{_ts()}.json', _json_bytes(_recipes_payload()))
        zf.writestr(f'configurazione_{_ts()}.json', _json_bytes(_config_payload()))
        if os.path.isdir(UPLOAD_FOLDER):
            for fname in os.listdir(UPLOAD_FOLDER):
                fpath = os.path.join(UPLOAD_FOLDER, fname)
                if os.path.isfile(fpath):
                    zf.write(fpath, os.path.join('immagini', fname))
    buf.seek(0)
    return send_file(buf, mimetype='application/zip', as_attachment=True,
                     download_name=f'backup_completo_{_ts()}.zip')


# ─────────────────────────────────────────────
# Import
# ─────────────────────────────────────────────

@backup_bp.route('/import', methods=['POST'])
@login_required
def import_backup():
    file = request.files.get('backup_file')
    mode = request.form.get('import_mode', 'merge')

    if not file or file.filename == '':
        flash("Nessun file selezionato.", "warning")
        return redirect(url_for('backup.backup_page'))

    filename = file.filename.lower()
    try:
        if filename.endswith('.json'):
            data = json.loads(file.read().decode('utf-8'))
            _import_json(data, mode)
        elif filename.endswith('.zip'):
            with zipfile.ZipFile(io.BytesIO(file.read())) as zf:
                for name in zf.namelist():
                    if name.endswith('.json'):
                        data = json.loads(zf.read(name).decode('utf-8'))
                        _import_json(data, mode)
                    elif name.startswith('immagini/') and not name.endswith('/'):
                        img_name = os.path.basename(name)
                        dest = os.path.join(UPLOAD_FOLDER, img_name)
                        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                        with open(dest, 'wb') as f:
                            f.write(zf.read(name))
        else:
            flash("Formato file non supportato. Usa .json o .zip.", "danger")
            return redirect(url_for('backup.backup_page'))

        flash("Ripristino completato con successo.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Errore durante l'importazione: {e}", "danger")

    return redirect(url_for('backup.backup_page'))


def _import_json(data, mode):
    btype = data.get('type')
    if btype == 'recipes':
        _import_recipes(data.get('recipes', []), mode)
    elif btype == 'config':
        _import_config(data, mode)
    else:
        raise ValueError(f"Tipo di backup non riconosciuto: {btype}")


def _import_recipes(recipes, mode):
    if mode == 'replace':
        RecipeIngredient.query.delete()
        RecipeFeature.query.delete()
        Recipe.query.delete()
        db.session.commit()

    for rd in recipes:
        existing = Recipe.query.filter_by(slug=rd['slug']).first()
        if existing and mode == 'merge':
            continue

        r = Recipe(
            name=rd['name'],
            slug=rd['slug'],
            badge_text=rd.get('badge_text', ''),
            description=rd.get('description', ''),
            instructions=rd.get('instructions', ''),
            icon=rd.get('icon', 'bi-journal-text'),
            is_published=rd.get('is_published', True),
            temp_chiusura=rd.get('temp_chiusura', 24.0),
            tempo_autolisi=rd.get('tempo_autolisi', 0),
            tempo_puntata=rd.get('tempo_puntata', 120),
            tempo_appretto=rd.get('tempo_appretto', 60),
            show_chiusura=rd.get('show_chiusura', True),
            show_autolysis=rd.get('show_autolysis', True),
            show_puntata=rd.get('show_puntata', True),
            puntata_fino_al_raddoppio=rd.get('puntata_fino_al_raddoppio', False),
            show_appretto=rd.get('show_appretto', True),
            fermentation_type=rd.get('fermentation_type', 'diretto'),
            preferment_instructions=rd.get('preferment_instructions', ''),
            yeast_ratio=rd.get('yeast_ratio', 3.0),
            yeast_fresh_saved=rd.get('yeast_fresh_saved', 3.0),
            yeast_dry_saved=rd.get('yeast_dry_saved', 1.0),
        )
        db.session.add(r)
        db.session.flush()

        for pan_name in rd.get('pans', []):
            pan = MasterBakeryPan.query.filter_by(name=pan_name).first()
            if pan:
                r.pans.append(pan)

        for idx, ing_d in enumerate(rd.get('ingredients', [])):
            ing = RecipeIngredient(
                recipe_id=r.id,
                name=ing_d['name'],
                quantity=ing_d.get('quantity', 0),
                percentage=ing_d.get('percentage', 0),
                unit=ing_d.get('unit', 'g'),
                is_flour=ing_d.get('is_flour', False),
                is_liquid=ing_d.get('is_liquid', False),
                w_value=ing_d.get('w_value', 0),
                is_optional=ing_d.get('is_optional', False),
                sort_order=ing_d.get('sort_order', idx),
                notes=ing_d.get('notes', ''),
            )
            db.session.add(ing)

        fd = rd.get('features', {})
        if fd:
            feat = RecipeFeature(
                recipe_id=r.id,
                enable_piece_count=fd.get('enable_piece_count', False),
                enable_piece_weight=fd.get('enable_piece_weight', False),
                enable_pans=fd.get('enable_pans', False),
                enable_hydration=fd.get('enable_hydration', False),
                enable_yeast_type=fd.get('enable_yeast_type', False),
                enable_tangzhong=fd.get('enable_tangzhong', False),
                enable_poolish=fd.get('enable_poolish', False),
                enable_biga=fd.get('enable_biga', False),
                enable_sourdough=fd.get('enable_sourdough', False),
                enable_baker_percentage=fd.get('enable_baker_percentage', True),
            )
            db.session.add(feat)

    db.session.commit()


def _import_config(data, mode):
    s_data = data.get('settings', {})
    s = Setting.query.first()
    if not s:
        s = Setting()
        db.session.add(s)

    s.fresh_to_dry_ratio = s_data.get('fresh_to_dry_ratio', s.fresh_to_dry_ratio)
    s.tangzhong_flour_percent = s_data.get('tangzhong_flour_percent', s.tangzhong_flour_percent)
    s.tangzhong_liquid_multiplier = s_data.get('tangzhong_liquid_multiplier', s.tangzhong_liquid_multiplier)
    s.site_name = s_data.get('site_name', s.site_name)
    s.site_description = s_data.get('site_description', s.site_description)
    s.default_unit = s_data.get('default_unit', s.default_unit)
    s.allow_public_recipes = s_data.get('allow_public_recipes', s.allow_public_recipes)
    s.theme_active = s_data.get('theme_active', s.theme_active)

    if mode == 'replace':
        MasterIngredient.query.delete()
        MasterBakeryPan.query.delete()
        WikiArticle.query.delete()

    for i_data in data.get('master_ingredients', []):
        if not MasterIngredient.query.filter_by(name=i_data['name']).first():
            db.session.add(MasterIngredient(
                name=i_data['name'],
                is_flour=i_data.get('is_flour', False),
                is_liquid=i_data.get('is_liquid', False),
                w_value=i_data.get('w_value', 0),
            ))

    for p_data in data.get('master_pans', []):
        if not MasterBakeryPan.query.filter_by(name=p_data['name']).first():
            db.session.add(MasterBakeryPan(
                name=p_data['name'],
                pan_type=p_data.get('pan_type', 'rettangolare'),
                weight_capacity=p_data.get('weight_capacity', 0.0),
            ))

    for w_data in data.get('wiki_articles', []):
        if not WikiArticle.query.filter_by(slug=w_data['slug']).first():
            db.session.add(WikiArticle(
                title=w_data['title'],
                slug=w_data['slug'],
                content=w_data.get('content', ''),
                category=w_data.get('category', 'Generale'),
            ))

    db.session.commit()
