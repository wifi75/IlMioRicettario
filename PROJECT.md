# PROGETTO: Il Mio Ricettario (V1 - Milestone v1.2.0)

## PANORAMICA
* **Nome:** Il Mio Ricettario
* **Versione:** V1 (In sviluppo attivo)
* **Milestone Corrente:** v1.2.0 - Integrazione Forza (W) Farine, Anagrafica Teglie, Theming Estetico e Sicurezza completati.
* **Repository GitHub:** https://github.com/wifi75/IlMioRicettario

---

## DESCRIZIONE & OBIETTIVI
Il Mio Ricettario è una piattaforma web professionale per la gestione di ricette dinamiche, focalizzata sul mondo dei lievitati (Pane, Pizza, Focacce, Panini, Grandi Lievitati). A differenza di un ricettario statico, ogni ricetta può attivare moduli e motori di calcolo configurabili dal backend (basati sulla Percentuale del Fornaio) che espongono interfacce interattive di ricalcolo in tempo reale nel frontend.

---

## STACK TECNOLOGICO
* **Backend:** Python 3 + Flask (Flask-SQLAlchemy, Flask-Login)
* **Database:** SQLite
* **Frontend:** Bootstrap 5, Bootstrap Icons, HTML5, CSS3, JavaScript (Vanilla)
* **Editor di Testo:** Quill.js v1.3.6 (Editor WYSIWYG integrato nei form)
* **Motore di Template:** Jinja2

---

## ARCHITETTURA DEI MODULI (FEATURES)
Ogni ricetta può abilitare o disabilitare funzionalità specifiche (Features) tramite interruttori nel pannello admin, salvati nel modello `RecipeFeature`:

1. **Modulo Panetti / Pezzature:** Configurazione di Numero Pezzi e Peso Singolo Pezzo.
2. **Modulo Teglie / Stampi:** Calcolo della quantità di impasto necessaria basata sulla capacità in grammi delle teglie (attinto dalla flotta globale `MasterBakeryPan`).
3. **Modulo Lievito & Conversioni:** Scelta dell'agente lievitante (Fresco, Secco Caputo, o Madre). La proporzione di conversione (Ratio) è definita globalmente nelle impostazioni.
4. **Modulo Tangzhong (Water Roux):** Sottrae automaticamente una percentuale di farina e un moltiplicatore di liquido dall'impasto principale per isolarli in una sezione dedicata (i coefficienti sono modificabili globalmente).
5. **Moduli Avanzati (Pre-impasti):** Gestione e calcolo automatizzato di Poolish (100% idro) e Biga (44% idro).

---

## STRUTTURA DATABASE (MODELLI SQLALCHEMY)
* `User`: Amministratori e credenziali di accesso. Password protette da hash crittografico (`password_hash`).
* `MasterIngredient`: Dizionario centralizzato degli ingredienti (ID, nome, flag `is_flour`, flag `is_liquid`, `w_value` per la forza).
* `MasterBakeryPan`: Anagrafica centralizzata delle teglie e degli stampi (nome, tipologia, capacità in grammi).
* `Recipe`: Testata della ricetta (titolo, istruzioni, idratazione target, tempi di processo). Include la relazione Many-to-Many con le teglie assegnate.
* `RecipeIngredient`: Ingredienti associati alla singola ricetta con metadati cristallizzati (quantità, unità, ordine, flag tecnici, `w_value`).
* `RecipeFeature`: Flag booleani per abilitare/disabilitare i singoli motori di calcolo sulla ricetta.
* `RecipeParameter`: Parametri di configurazione locali della ricetta (es. peso panetto impostato).
* `Setting`: Configurazione globale dei parametri del sito (rapporto lieviti, parametri tangzhong, `site_name`, `site_description`, `theme_active`).
* `WikiArticle`: Articoli enciclopedici della sezione Wiki (CRUD completo).

---

## REGOLE DI SVILUPPO (TASSATIVE)
1. **File Completi:** Fornire sempre codici interi pronti al copia-incolla per evitare frammentazioni o omissioni. No patch parziali o commenti placeholder.
2. **Nessun Loop nel Database:** Non appesantire il Context Processor globale (`@app.context_processor`) con query dinamiche o pesanti. Passare i dati esplicitamente tramite i Blueprint.
3. **Isolamento Condizionale:** Mantenere i tag condizionali di Jinja (`{% if %}`) strutturalmente solidi e bilanciati per non interrompere il rendering dell'HTML (`base.html`).
4. **Mobile First & UI:** Layout pulito, responsive con classi native di Bootstrap 5. Interfaccia scura per la sidebar admin e card bianche minimaliste su sfondo slate leggero per i contenuti.

---

## LOGICHE OPERATIVE CHIAVE (DA PRESERVARE TASSATIVAMENTE)
1. **Integrazione Quill.js:** Al submit dei form di creazione/modifica ricetta, un listener JavaScript cattura il testo lineare (`quill.getText().trim()`) e lo inietta in un input hidden `name="instructions"`.
2. **Parsing Istruzioni Frontend:** Nel rendering del dettaglio ricetta, il testo delle istruzioni viene elaborato dinamicamente via Jinja2 (`.split('\n')`), generando un elenco numerato progressivo automatico e formattando in grassetto (`<strong>`) la prima parola di ogni riga.
3. **Gestione della Forza (W) delle Farine:** Il valore della forza viene censito centralmente. Nel form della ricetta, JavaScript preleva il W dal `<datalist>` e lo inserisce in un array nascosto `ing_w[]`. Python lo intercetta nel POST e lo storicizza in `RecipeIngredient`. Sul frontend, il badge `W` appare visivamente SOLO se l'ingrediente ha il flag `is_flour` attivo.

---

## STATO ATTUALE (COMPLETATO & COLLAUDATO SU GIT)
* **Autenticazione & Sicurezza:** Login/Logout funzionante con account di fabbrica automatico (`admin`/`admin123`). Schermata "Sicurezza Account" attiva per hash sicuro.
* **Layout Base Consolidato:** Tasto di navigazione admin spostato logicamente nel footer sul sito pubblico.
* **Anagrafica Centralizzata Ingredienti:** Tabella `MasterIngredient` attiva. Form interbloccato JS (impedisce flag farina e liquido contemporanei).
* **Forza delle Farine (W):** Sincronizzazione perfetta del parametro W dal DB centrale alla ricetta locale. UI pulita (nessun badge "—" per sale, acqua, ecc.).
* **Flotta Teglie:** Creata anagrafica globale `MasterBakeryPan` e sistema di assegnazione multipla sulle ricette. Interfaccia calcolatore frontend ottimizzata con tasti +/- puliti.
* **Core Calcoli:** Calcolo dinamico in tempo reale di farine, liquidi e idratazione reale.
* **Personalizzazione Globale:** Implementato il salvataggio dei testi istituzionali e dei temi estetici CSS direttamente nel database `Setting`.
* **Git & Backup:** Working tree pulito, cartella `instance/`, file `.db` e cache Python esclusi in sicurezza tramite `.gitignore`.