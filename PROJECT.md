# CHATGPT CONTEXT (V1 - Milestone v1.1.0)

## PROGETTO
* **Nome:** Il Mio Ricettario
* **Versione:** V1 (In sviluppo attivo)
* **Milestone Corrente:** v1.1.0 - Core calcoli, Editor avanzato e Sicurezza completati.
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
2. **Modulo Teglie / Stampi:** Calcolo della quantità di impasto necessaria basata sulla superficie di teglie rettangolari o tonde.
3. **Modulo Lievito & Conversioni:** Scelta dell'agente lievitante (Fresco, Secco Caputo, o Madre). La proporzione di conversione (Ratio) è definita globalmente nelle impostazioni.
4. **Modulo Tangzhong (Water Roux):** Sottrae automaticamente il 5% della farina totale e un moltiplicatore 5× di liquido dall'impasto principale per isolarli in una sezione dedicata (i coefficienti sono modificabili globalmente).
5. **Moduli Avanzati (Pre-impasti):** Gestione e calcolo automatizzato di Poolish (100% idro) e Biga (44% idro).

---

## STRUTTURA DATABASE (MODELLI SQLALCHEMY)
* `User`: Amministratori e credenziali di accesso. Password protette da hash crittografico (`password_hash`).
* `MasterIngredient`: Dizionario centralizzato degli ingredienti (ID, nome, flag `is_flour`, flag `is_liquid`).
* `Recipe`: Testata della ricetta (titolo, istruzioni in testo lineare con `\n`, idratazione target, tempi di autolisi, puntata, appretto).
* `RecipeIngredient`: Ingredienti associati alla singola ricetta (quantità, unità, ordine, flag tecnici).
* `RecipeFeature`: Flag booleani per abilitare/disabilitare i singoli motori di calcolo sulla ricetta.
* `RecipeParameter`: Parametri di configurazione locali della ricetta (es. peso panetto impostato).
* `Setting`: Configurazione globale dei parametri del sito (rapporto lieviti, parametri tangzhong, unità di misura).
* `WikiArticle`: Articoli enciclopedici della sezione Wiki (CRUD completo).

---

## REGOLE DI SVILUPPO (TASSATIVE)
1. **File Completi:** Fornire sempre codici interi pronti al copia-incolla per evitare frammentazioni o omissioni. No patch parziali o commenti placeholder.
2. **Nessun Loop nel Database:** Non appesantire il Context Processor globale (`@app.context_processor`) con query dinamiche o pesanti che possono generare ricorsioni o blocchi di sessione. Passare i dati esplicitamente tramite i Blueprint.
3. **Isolamento Condizionale:** Mantenere i tag condizionali di Jinja (`{% if %}`) strutturalmente solidi e bilanciati per non interrompere il rendering dell'HTML (`base.html`).
4. **Mobile First & UI:** Layout pulito, responsive con classi native di Bootstrap 5. Interfaccia scura per la sidebar admin e card bianche minimaliste su sfondo slate leggero per i contenuti.

---

## LOGICHE OPERATIVE CHIAVE (DA PRESERVARE TASSATIVAMENTE)
1. **Integrazione Quill.js:** Al submit dei form di creazione/modifica ricetta, un listener JavaScript cattura il testo lineare (`quill.getText().trim()`) e lo inietta in un input hidden `name="instructions"` mantenendo solo i caratteri nativi di nuova riga (`\n`).
2. **Parsing Istruzioni Frontend:** Nel rendering del dettaglio ricetta, il testo delle istruzioni viene elaborato dinamicamente riga per riga via Jinja2 (`.split('\n')`), generando un elenco numerato progressivo automatico e formattando in grassetto (`<strong>`) la prima parola di ogni riga.
3. **Rotte Admin Scelte:** La rotta vecchio stile `/admin/dashboard` è permanentemente disattivata e reindirizza con un redirect sicuro 302 verso la gestione centrale delle ricette `/admin/recipes`.

---

## STATO ATTUALE (COMPLETATO & COLOGATO SU GIT)
* **Autenticazione & Sicurezza:** Login/Logout funzionante con account di fabbrica automatico (`admin`/`admin123`). Creata schermata "Sicurezza Account" per modificare la password con hashing sicuro direttamente dal pannello.
* **Layout Base Consolidato:** File `base.html` privo di bug strutturali, gestisce correttamente sidebar admin e isolamento degli utenti anonimi.
* **Anagrafica Centralizzata Ingredienti:** Tabella `MasterIngredient` attiva con seeding automatico di 13 ingredienti base all'avvio. Schermata `/admin/ingredients/master` completata con form di inserimento interbloccato JS (impedisce flag farina e liquido contemporanei) e tabella di rimozione.
* **Core Calcoli:** Calcolo dinamico in tempo reale di farine totali, liquidi totali e percentuale reale di idratazione dell'impasto nel backend amministrativo e nel frontend di visualizzazione.
* **Git & Backup:** Working tree pulito, cartella `instance/`, file `.db` e cache Python esclusi in sicurezza tramite `.gitignore`.