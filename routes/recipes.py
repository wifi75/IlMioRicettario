from flask import (
    Blueprint,
    render_template
)

from models.recipe import Recipe
from models.ingredient import RecipeIngredient
from models.feature import RecipeFeature

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


# 📚 =========================================================================
# ROTTA PUBBLICA DELLA WIKI (Blindata e Indipendente dal Database)
# =========================================================================
@recipes_bp.route("/wiki")
def wiki_public_list():
    # Generiamo il manuale direttamente da qui per evitare conflitti di importazione
    manuale_tecnico = {
        "title": "MANUALE UTENTE & LINEE GUIDA - L'ARTE BIANCA",
        "content": """
            <p>Benvenuto nella Wiki ufficiale del sistema di ricettario dinamico avanzato. Questo manuale è stato progettato per guidarti nella configurazione, nel bilanciamento e nella gestione ottimale delle formule di panificazione professionale.</p>
            
            <h4 class="mt-4 fw-bold text-dark">1. GESTIONE DEGLI INGREDIENTI E PERCENTUALE BAKER</h4>
            <ul>
                <li><strong>La Farina è il centro (100%):</strong> Nelle formule avanzate, la farina rappresenta sempre il 100%. Tutti gli altri ingredienti (acqua, lievito, sale, grassi) vengono calcolati in proporzione al peso totale della farina.</li>
                <li><strong>Inserimento dei Dati:</strong> Quando crei una ricetta nel pannello di amministrazione, inserisci le percentuali desiderate. Il sistema ricalcolerà istantaneamente i grammi in base alla quantità di impasto richiesta dall'utente.</li>
            </ul>

            <h4 class="mt-4 fw-bold text-dark">2. LA FORZA DELLA FARINA (W) E L'IDRATAZIONE</h4>
            <ul>
                <li><strong>Biscotti / Frolle:</strong> Forza W 90 - 130 | Idratazione: Bassa (Sotto il 45%)</li>
                <li><strong>Pane Diretto / Focacce:</strong> Forza W 180 - 240 | Idratazione: Media (55% - 65%)</li>
                <li><strong>Pizze in Teglia / Alta Idratazione:</strong> Forza W 260 - 320 | Idratazione: Alta (70% - 80%) | Lievitazione: 24 - 48 ore in Frigo.</li>
            </ul>

            <h4 class="mt-4 fw-bold text-dark">3. BILANCIAMENTO DINAMICO DELLE TEGLIE</h4>
            <p>Il programma applica il coefficiente matematico di occupazione della superficie: <strong>Peso Impasto (g) = Area della Teglia (cm²) x Coefficiente Spessore</strong></p>
            <ul>
                <li><strong>Focaccia Barese / Pizza Alta:</strong> Coefficiente 0.60 - 0.70</li>
                <li><strong>Pizza in Teglia alla Romana:</strong> Coefficiente 0.50 - 0.55</li>
            </ul>

            <h4 class="mt-4 fw-bold text-dark">4. BUONE PRATICHE PER L'AMMINISTRATORE</h4>
            <ol>
                <li><strong>Nomi delle Ricette:</strong> Utilizza sempre il testo in MAIUSCOLO (es. FOCACCIA BARESE). Garantisce l'inserimento perfetto nei blocchi delle card.</li>
                <li><strong>Immagini di Copertina:</strong> Preferisci immagini con sfondo chiaro o trasparente. Il programma eliminerà automaticamente gli stacchi di colore.</li>
            </ol>
        """
    }
    
    # Passiamo il manuale finto come lista per non toccare il file HTML
    return render_template(
        "wiki_public.html",
        wiki_articles=[manuale_tecnico]
    )