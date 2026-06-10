===================================================================
CONTEXT DI PROGETTO: "IL MIO RICETTARIO" (Aggiornato: Giugno 2026)
==================================================================

PROGETTO

* Nome: Il Mio Ricettario
* Sviluppatore Principale: Tiziano Cassone
* Versione Architetturale: v2.2.0 (Stabile)
* Repository GitHub: https://github.com/wifi75/IlMioRicettario

---

## STACK TECNOLOGICO CORRENTE

Backend

* Python 3.13
* Flask 3.1.2
* Flask-SQLAlchemy 3.1.1
* Flask-Login 0.6.3
* Flask-Migrate 4.1.0
* Werkzeug 3.1.3

Database

* SQLite

Frontend

* Bootstrap 5.3
* Bootstrap Icons
* HTML5
* CSS3
* JavaScript Vanilla

Editor

* Quill.js v1.3.6

Documentazione PDF

* ReportLab 4.4.3

Template Engine

* Jinja2

---

## STATO STRUTTURALE DEL LAYOUT & LEGGE CROMATICA (V2)

1. BASE GRAPHIC DESIGN

* Lo sfondo del body è fissato su:

  #f8fafc

* Tutti i temi chiari devono mantenere questo colore come riferimento.

* Il tema "forno_paese" utilizza testi scuri ad alto contrasto per garantire la massima leggibilità.

---

2. HERO HEADER PUBBLICO (recipes_list.html)

* Contenitore bianco compatto.

* Larghezza massima:

  850px

* L'icona della spiga 🌾 è posizionata tramite:

  position: absolute;
  left: 24px;
  top: 50%;
  transform: translateY(-50%);

* Titolo e descrizione devono rimanere geometricamente centrati.

---

3. BADGE W E TAG CONDIZIONALI

Tutti i badge devono utilizzare:

```
display: inline-flex !important;
align-items: center !important;
justify-content: center !important;
```

per garantire l'allineamento perfetto del contenuto.

---

## ARCHITETTURA DATABASE (MODELLI SQLALCHEMY)

User

* Gestione utenti amministratori.
* Password protette tramite password_hash.
* Autenticazione Flask-Login.

---

MasterIngredient

Anagrafica ingredienti centralizzata.

Campi principali:

* id
* name
* is_flour
* is_liquid
* w_value

Popolamento automatico tramite seeding.

---

MasterBakeryPan

Anagrafica teglie e stampi.

Campi principali:

* id
* name
* pan_type
* weight_capacity

Utilizzata tramite relazione Many-to-Many con Recipe.

---

MasterImage

Nuovo modello introdotto nella v2.2.0.

Archivio immagini centralizzato.

Campi principali:

* id
* filename
* caption
* alt_text
* upload_date

Funzioni:

* archivio unico immagini;
* riutilizzo su più ricette;
* anteprima dinamica;
* associazione persistente.

---

Recipe

Testata principale della formula.

Campi principali:

* id
* name
* slug
* description
* instructions
* image
* image_id
* temp_chiusura
* tempo_autolisi
* tempo_puntata
* tempo_appretto

Relazioni:

* RecipeIngredient
* RecipeFeature
* MasterBakeryPan
* MasterImage

---

RecipeIngredient

Relazione ingredienti ↔ ricette.

Metadati:

* quantity
* unit
* is_flour
* is_liquid
* w_value
* sort_order

---

RecipeFeature

Abilitazione dinamica dei moduli:

* enable_piece_count
* enable_piece_weight
* enable_yeast_type
* enable_tangzhong
* enable_poolish
* enable_biga

---

Setting

Parametri globali applicazione.

Include:

* fresh_to_dry_ratio
* tangzhong_flour_percent
* tangzhong_liquid_multiplier
* site_name
* site_description
* theme_active

---

wiki

Classe definita in:

```
models/wiki.py
```

Il nome della classe rimane volutamente:

```
wiki
```

(interamente minuscolo).

---

## LOGICHE OPERATIVE CRITICHE (DA PRESERVARE)

1. WIKI PUBBLICA IMMORTALE

Rotta:

```
/wiki
```

Gestita tramite:

```
routes/recipes.py
```

Funzione:

```
wiki_public_list()
```

La Wiki deve continuare a funzionare anche in caso di:

* assenza tabelle;
* problemi del modello wiki;
* database incompleto.

Il contenuto base viene precaricato tramite dizionario Python.

---

2. QUILL.JS

Nei form di creazione e modifica ricetta:

* Quill.js gestisce l'editor.
* Il testo viene salvato tramite:

  name="instructions"

all'interno di un campo hidden.

---

3. PARSING DELLE ISTRUZIONI

Le istruzioni vengono elaborate tramite:

```
.split('\n')
```

e convertite automaticamente in:

* elenco numerato;
* prima parola in grassetto.

---

4. GESTIONE FORZA W

Il valore W:

* viene letto da MasterIngredient;
* viene copiato in RecipeIngredient;
* viene storicizzato nella ricetta.

Il badge W deve apparire solamente sugli ingredienti marcati come farine.

---

5. SISTEMA IMMAGINI CENTRALIZZATO

Nuova architettura v2.2.0.

Le immagini vengono gestite tramite:

```
MasterImage
```

e collegate alle ricette tramite:

```
Recipe.image_id
```

Backend:

* selezione tramite dropdown;
* anteprima dinamica;
* pulsante applica;
* pulsante scollega.

L'associazione deve persistere dopo il salvataggio.

Non devono essere reintrodotti sistemi basati su elenchi completi di miniature.

---

6. PROTEZIONE DATI LOCALI

Il file .gitignore deve escludere:

```
instance/
*.db
__pycache__/
*.pyc
```

---

## REGOLE PER LE FUTURE AI IN CHAT

1. Fornire SEMPRE file completi.

Mai fornire:

* patch parziali;
* placeholder;
* sezioni omesse.

---

2. Mantenere sempre la firma:

   Architettato e sviluppato da Tiziano Cassone

nel footer amministrativo.

---

3. Non inserire query pesanti dentro:

   @app.context_processor

Le query devono essere eseguite esclusivamente:

* nelle rotte;
* nei blueprint;
* nei servizi dedicati.

---

4. Prima di modificare la gestione immagini verificare sempre:

* modello Recipe;
* modello MasterImage;
* routes/admin.py;
* recipe_form.html;

poiché la selezione immagini è ora basata sul collegamento:

```
Recipe.image_id
```

e non più sul solo campo:

```
Recipe.image
```

---

## FINE CONTESTO
