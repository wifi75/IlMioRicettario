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
# IMPORTAZIONE NUOVO MODELLO DELLE TEGLIE MASTER
from models.bakery_pan import MasterBakeryPan
# IMPORTAZIONE NUOVO MODELLO IMMAGINI MASTER
from models.image import MasterImage

from routes.recipes import recipes_bp
from routes.admin import admin_bp
from routes.backup import backup_bp


app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)
login_manager.init_app(app)

# INIZIALIZZAZIONE DEL MOTORE DI MIGRAZIONE DEL DATABASE
migrate = Migrate(app, db)

# ==========================================================
# CRITICO: NUOVO ORDINE DI REGISTRAZIONE BLUEPRINT
# ==========================================================
app.register_blueprint(admin_bp)
app.register_blueprint(recipes_bp)
app.register_blueprint(backup_bp)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(
        User,
        int(user_id)
    )


# CORRETTO: Ordiniamo per ID decrescente per prendere SICURAMENTE l'ultimo record attivo e aggiornato
@app.context_processor
def inject_global_settings():
    setting_record = Setting.query.order_by(Setting.id.desc()).first()
    return dict(
        settings_data=setting_record
    )


@app.route("/")
def index():
    return redirect(
        url_for("recipes.list_recipes")
    )


with app.app_context():
    try:
        db.session.execute(db.text("ALTER TABLE recipes ADD COLUMN yeast_fresh_saved REAL DEFAULT 3.0"))
        db.session.execute(db.text("ALTER TABLE recipes ADD COLUMN yeast_dry_saved REAL DEFAULT 1.0"))
        db.session.commit()
        print("Allineamento colonne lievito personalizzato completato!")
    except Exception:
        db.session.rollback()    

    db.create_all()

    
    # =========================================================================
    # DA QUI IN POI LE QUERY POSSONO GIRARE IN TOTALE SICUREZZA
    # =========================================================================
    admin = User.query.filter_by(
        username="admin"
    ).first()

    if not admin:
        import secrets
        import string
        alphabet = string.ascii_letters + string.digits + "!#$%&*+"
        generated_password = ''.join(secrets.choice(alphabet) for _ in range(16))

        admin = User(
            username="admin",
            password_hash=generate_password_hash(generated_password),
            is_admin=True
        )

        db.session.add(admin)
        db.session.commit()

        print("=" * 50)
        print("ADMIN CREATO — PRIMA INSTALLAZIONE")
        print(f"Username: admin")
        print(f"Password: {generated_password}")
        print("Accedi e cambiala subito da /admin/change_password")
        print("=" * 50)

    if MasterBakeryPan.query.count() == 0:
        default_pans = [
            MasterBakeryPan(name="Teglia Rettangolare Ferro Blu 40x30", pan_type="rettangolare", weight_capacity=1200.0),
            MasterBakeryPan(name="Tonda Classica Diametro 32", pan_type="rotonda", weight_capacity=650.0),
            MasterBakeryPan(name="Stampo Panettone Alto 1kg", pan_type="stampo", weight_capacity=1000.0)
        ]
        db.session.bulk_save_objects(default_pans)
        db.session.commit()

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

    if WikiArticle.query.count() == 0:
        wiki_seed = [
            WikiArticle(
                title="Come Funziona il Calcolatore di Ricette",
                slug="come-funziona-il-calcolatore",
                category="Guida",
                content=(
                    "<h2>Il Sistema di Calcolo</h2>"
                    "<p>Il calcolatore integrato in ogni ricetta ridimensiona automaticamente tutti gli ingredienti "
                    "in base al risultato desiderato. Sono disponibili tre modalità selezionabili dal menu "
                    "<strong>Metodo di Calcolo</strong> in cima alla scheda ricetta.</p>"
                    "<h3>Peso Impasto Desiderato</h3>"
                    "<p>Inserisci il peso totale dell'impasto che vuoi ottenere (es. 1000 g). "
                    "Il sistema ridimensiona proporzionalmente tutti gli ingredienti mantenendo invariate "
                    "le percentuali della formula originale.</p>"
                    "<h3>Calcolo per Pezzature</h3>"
                    "<p>Indica il numero di pezzi e il peso unitario (es. 8 panetti da 250 g). "
                    "Il totale impasto viene calcolato automaticamente e la formula viene scalata di conseguenza.</p>"
                    "<h3>Calcolo per Teglie</h3>"
                    "<p>Se la ricetta ha teglie associate, usa i pulsanti + e − per impostare quante teglie "
                    "vuoi riempire. Il peso impasto viene calcolato sulla base della capacità di ogni teglia.</p>"
                    "<h3>Regola Fondamentale</h3>"
                    "<p>Il peso mostrato al primo caricamento è sempre il peso reale della ricetta originale. "
                    "Non viene mai alterato automaticamente dalla cache del browser.</p>"
                )
            ),
            WikiArticle(
                title="La Percentuale Baker (Baker's Percentage)",
                slug="percentuale-baker",
                category="Tecnica",
                content=(
                    "<h2>Cos'è la Percentuale Baker</h2>"
                    "<p>La percentuale baker è il sistema professionale usato in panificazione per esprimere "
                    "la quantità di ogni ingrediente in rapporto al peso totale delle farine, che per "
                    "convenzione vale sempre 100%.</p>"
                    "<h3>Esempio Pratico</h3>"
                    "<p>Formula con 1000 g di farina e 700 g di acqua:</p>"
                    "<ul><li>Farina: 100%</li><li>Acqua: 70% (700 ÷ 1000 × 100)</li>"
                    "<li>Sale: 2% = 20 g</li><li>Lievito: 0,3% = 3 g</li></ul>"
                    "<h3>Perché è Utile</h3>"
                    "<p>Con la percentuale baker puoi confrontare ricette di dimensioni diverse, "
                    "capire l'equilibrio di una formula e scalare qualsiasi impasto senza calcoli manuali.</p>"
                    "<h3>Nel Calcolatore</h3>"
                    "<p>La colonna <strong>Percentuale Baker</strong> è visibile su tablet e desktop. "
                    "Su smartphone viene nascosta per massimizzare la leggibilità, "
                    "mostrando solo Materia Prima, Forza (W) e Grammi.</p>"
                )
            ),
            WikiArticle(
                title="Idratazione dell'Impasto",
                slug="idratazione-impasto",
                category="Tecnica",
                content=(
                    "<h2>Cos'è l'Idratazione</h2>"
                    "<p>L'idratazione esprime il rapporto tra il peso totale dei liquidi e il peso totale "
                    "delle farine, in percentuale. Determina la consistenza dell'impasto e "
                    "le caratteristiche del prodotto finito.</p>"
                    "<h3>Formula</h3>"
                    "<p><strong>Idratazione (%) = (Liquidi totali ÷ Farine totali) × 100</strong></p>"
                    "<h3>Valori di Riferimento</h3>"
                    "<ul>"
                    "<li><strong>55–65%</strong> — Impasti sodi: grissini, pasta di pane classica</li>"
                    "<li><strong>65–75%</strong> — Impasti morbidi: pane comune, panini, focaccia leggera</li>"
                    "<li><strong>75–85%</strong> — Impasti molli: ciabatta, pizza napoletana</li>"
                    "<li><strong>85–100%+</strong> — Impasti liquidissimi: bâtard, focaccia genovese</li>"
                    "</ul>"
                    "<h3>Lo Slider Idratazione</h3>"
                    "<p>Attivando <em>Consenti ricalcolo idratazione personalizzato</em> puoi modificare "
                    "l'idratazione tramite lo slider. I liquidi vengono ridistribuiti automaticamente "
                    "mantenendo invariata la quantità delle farine.</p>"
                )
            ),
            WikiArticle(
                title="Gestione Pezzature e Porzioni",
                slug="pezzature-porzioni",
                category="Guida",
                content=(
                    "<h2>Calcolo per Pezzatura</h2>"
                    "<p>Il modulo pezzatura calcola il peso impasto necessario partendo dal numero "
                    "di pezzi desiderati e dal peso unitario di ciascuno.</p>"
                    "<h3>Come Si Usa</h3>"
                    "<ol>"
                    "<li>Seleziona <strong>Calcolo per N. Pezzi e Peso</strong> dal menu Metodo di Calcolo.</li>"
                    "<li>Inserisci il numero di pezzi nel campo <strong>Pezzi</strong>.</li>"
                    "<li>Inserisci il peso desiderato per ogni pezzo in grammi.</li>"
                    "<li>Il calcolatore aggiorna automaticamente tutti gli ingredienti.</li>"
                    "</ol>"
                    "<h3>Esempio</h3>"
                    "<p>12 panini da 80 g ciascuno → 12 × 80 = 960 g totali. "
                    "La formula viene scalata di conseguenza.</p>"
                    "<h3>Nota sul Peso</h3>"
                    "<p>Il peso per pezzatura si riferisce all'impasto crudo. "
                    "Il prodotto cotto perderà circa il 10–15% per evaporazione.</p>"
                )
            ),
            WikiArticle(
                title="Calcolo per Teglie",
                slug="calcolo-teglie",
                category="Guida",
                content=(
                    "<h2>Il Sistema Teglie</h2>"
                    "<p>Ogni ricetta può avere associate una o più teglie dall'anagrafica. "
                    "Il calcolo per teglie determina il peso totale impasto in base alla capacità "
                    "di ogni teglia e alla quantità selezionata.</p>"
                    "<h3>Come Si Usa</h3>"
                    "<ol>"
                    "<li>Seleziona <strong>Calcolo per Teglie Assegnate</strong> dal menu.</li>"
                    "<li>Usa i pulsanti <strong>+</strong> e <strong>−</strong> per ogni teglia.</li>"
                    "<li>Il totale impasto = somma delle capacità × quantità.</li>"
                    "</ol>"
                    "<h3>Anagrafica Teglie</h3>"
                    "<p>Le teglie si gestiscono nel pannello admin sotto <em>Anagrafica Teglie</em>. "
                    "Per ogni teglia si definisce il nome e la capacità in grammi. "
                    "Le teglie vengono poi associate alle singole ricette nel form di modifica.</p>"
                )
            ),
            WikiArticle(
                title="Tangzhong e Roux",
                slug="tangzhong-roux",
                category="Tecnica",
                content=(
                    "<h2>Cos'è il Tangzhong</h2>"
                    "<p>Il Tangzhong è una tecnica di panificazione asiatica che consiste nel precuocere "
                    "una piccola percentuale di farina con i liquidi fino a ottenere una crema gelatinosa "
                    "(roux). Questo gel viene poi incorporato nell'impasto principale, migliorando "
                    "morbidezza e conservabilità del prodotto.</p>"
                    "<h3>Perché Funziona</h3>"
                    "<p>A 65°C gli amidi gelatinizzano e legano grandi quantità di acqua in forma stabile. "
                    "Quest'acqua non evapora durante la cottura, mantenendo la mollica umida anche "
                    "nei giorni successivi alla sfornatura.</p>"
                    "<h3>Come Si Prepara</h3>"
                    "<ol>"
                    "<li>Pesa i grammi indicati nella tab <em>Roux/Tangzhong</em>.</li>"
                    "<li>Mescola farina e liquido a freddo in un pentolino.</li>"
                    "<li>Scalda mescolando fino a crema densa (circa 65°C).</li>"
                    "<li>Lascia raffreddare prima di aggiungere all'impasto.</li>"
                    "</ol>"
                    "<h3>Nel Calcolatore</h3>"
                    "<p>I grammi di farina e liquido del Tangzhong vengono <strong>scorporati automaticamente</strong> "
                    "dalla formula principale. La tab <em>Roux/Tangzhong</em> mostra i valori già sottratti.</p>"
                    "<h3>Proporzioni Standard</h3>"
                    "<p>Configurazione predefinita: <strong>5% della farina totale</strong> con liquidi "
                    "pari a <strong>5× la farina del roux</strong>. Valori modificabili dal pannello admin.</p>"
                )
            ),
            WikiArticle(
                title="Prefermenti: Poolish e Biga",
                slug="poolish-biga",
                category="Tecnica",
                content=(
                    "<h2>I Prefermenti</h2>"
                    "<p>I prefermenti sono impasti preparati 12–16 ore prima che vengono incorporati "
                    "nell'impasto finale. Migliorano il profilo aromatico, la digeribilità e "
                    "la struttura del prodotto.</p>"
                    "<h2>Poolish</h2>"
                    "<p>Prefermento liquido di origine polacca con idratazione al <strong>100%</strong> "
                    "(pesi uguali di farina e acqua). Ideale per pane con alveolatura aperta, "
                    "baguette e pizza napoletana.</p>"
                    "<h3>Proporzioni Poolish</h3>"
                    "<ul>"
                    "<li>Farina: 30% della farina totale della ricetta</li>"
                    "<li>Acqua: uguale alla farina (idratazione 100%)</li>"
                    "<li>Lievito: tutto il lievito della formula</li>"
                    "</ul>"
                    "<h2>Biga</h2>"
                    "<p>Prefermento solido di origine italiana con idratazione al <strong>44%</strong>. "
                    "Ideale per pane pugliese, ciabatta e prodotti con struttura robusta.</p>"
                    "<h3>Proporzioni Biga</h3>"
                    "<ul>"
                    "<li>Farina: 100% della farina totale della ricetta</li>"
                    "<li>Acqua: 44% rispetto alla farina della biga</li>"
                    "<li>Lievito: tutto il lievito della formula</li>"
                    "</ul>"
                    "<h3>Nel Calcolatore</h3>"
                    "<p>Con il modulo prefermento attivo, la tab <em>Prefermento</em> mostra i grammi "
                    "di farina, acqua e lievito da preparare in anticipo, già <strong>scorporati</strong> "
                    "dalla formula principale.</p>"
                )
            ),
            WikiArticle(
                title="Conversione Lieviti",
                slug="conversione-lieviti",
                category="Guida",
                content=(
                    "<h2>Lievito Fresco e Lievito Secco</h2>"
                    "<p>Il selettore lievito converte automaticamente le dosi tra lievito di birra fresco "
                    "e lievito di birra secco disidratato.</p>"
                    "<h3>Rapporto di Conversione</h3>"
                    "<p>Rapporto predefinito <strong>3:1</strong> — 3 g di lievito fresco = 1 g di lievito secco. "
                    "Il valore è configurabile dal pannello admin nelle Impostazioni di Sistema.</p>"
                    "<h3>Esempio</h3>"
                    "<p>Formula con 6 g di lievito fresco → equivale a 2 g di lievito secco (6 ÷ 3).</p>"
                    "<h3>Come Si Usa</h3>"
                    "<ol>"
                    "<li>Nella scheda ricetta seleziona <em>Lievito fresco</em> o <em>Lievito secco disidratato</em>.</li>"
                    "<li>Il calcolatore converte la dose mantenendo invariato il potere lievitante.</li>"
                    "<li>La scelta viene memorizzata nel browser per le sessioni successive.</li>"
                    "</ol>"
                    "<h3>Note di Utilizzo</h3>"
                    "<p>Il lievito secco va attivato in acqua tiepida (35–38°C) per 10 minuti prima dell'uso. "
                    "Il lievito fresco si sbriciola direttamente nella farina o nei liquidi.</p>"
                )
            ),
            WikiArticle(
                title="La Forza della Farina: il Valore W",
                slug="valore-w-farina",
                category="Tecnica",
                content=(
                    "<h2>Cos'è il Valore W</h2>"
                    "<p>Il valore W misura la forza del glutine di una farina, ovvero la sua capacità "
                    "di resistere alle sollecitazioni durante l'impastamento e la lievitazione. "
                    "Viene determinato con l'alveografo di Chopin.</p>"
                    "<h3>Classificazione delle Farine</h3>"
                    "<ul>"
                    "<li><strong>W 90–160</strong> — Farine deboli: biscotti, pasta frolla, cialde</li>"
                    "<li><strong>W 160–250</strong> — Farine medie: pane comune, pizza al taglio, grissini</li>"
                    "<li><strong>W 250–310</strong> — Farine forti: pane a lunga lievitazione, pizza napoletana</li>"
                    "<li><strong>W 310–400+</strong> — Farine speciali: panettone, pandoro, grandi lievitati</li>"
                    "</ul>"
                    "<h3>Nel Calcolatore</h3>"
                    "<p>Il valore W di ogni farina appare come badge nella colonna <strong>(W)</strong> "
                    "della tabella ingredienti. Visibile su tutti i dispositivi; su smartphone la colonna "
                    "è compatta con solo il valore numerico.</p>"
                    "<h3>Blending di Farine</h3>"
                    "<p>Miscelando farine con W diversi si ottiene un W intermedio calcolabile come "
                    "media ponderata: <strong>W blend = (W1 × g1 + W2 × g2) / (g1 + g2)</strong>. "
                    "Il calcolo automatico del W medio è previsto nella roadmap v3.</p>"
                )
            ),
        ]
        db.session.bulk_save_objects(wiki_seed)
        db.session.commit()
        print("Wiki tecnica seminata con 9 voci.")

    setting = Setting.query.first()

    if not setting:
        setting = Setting(
            fresh_to_dry_ratio=3.0,
            tangzhong_flour_percent=5.0,
            tangzhong_liquid_multiplier=5.0,
            site_name="Il Mio Ricettario",
            site_description="Esplora le nostre antiche formule bilanciate professionali. Utilizza i motori di calcolo integrati ad alta precisione per ridimensionare istantaneamente ogni impasto[...]",
            default_unit="g",
            allow_public_recipes=True,
            theme_active="modern"
        )
        db.session.add(setting)
        db.session.commit()
    else:
        try:
            db.session.execute(db.text("UPDATE settings SET theme_active = 'modern' WHERE theme_active IS NULL"))
            db.session.execute(db.text("UPDATE settings SET site_description = 'Esplora le nostre antiche formule bilanciate professionali. Utilizza i motori di calcolo integrati ad alta precisio[...]' WHERE site_description IS NULL"))
            db.session.commit()
        except Exception:
            db.session.rollback()
    import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

for directory in [
    "data",
    "static/uploads",
    "static/uploads/recipes"
]:
    os.makedirs(
        os.path.join(BASE_DIR, directory),
        exist_ok=True
    )

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=app.config.get("PORT", 8080),
        debug=False
    )
