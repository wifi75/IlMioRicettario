# CLAUDE.md — Il Mio Ricettario

## Lingua

Rispondi sempre in italiano, in ogni risposta e in ogni commento nel codice.

## Regole operative

- Non modificare alcun file senza esplicita conferma dell'utente.
- Prima di qualsiasi modifica, mostra sempre:
  - il piano completo dell'intervento
  - l'elenco di tutti i file coinvolti
  - il codice attuale e il codice proposto (non snippet parziali)
- Non modificare il database o i file di migrazione Alembic senza conferma esplicita.
- Non cancellare file, cartelle o record senza conferma esplicita.
- Esegui `git status` prima di qualsiasi intervento rilevante.

## Gestione modifiche

- Prima di modificare qualsiasi file mostra sempre un riepilogo:
  - file da modificare
  - motivo della modifica
  - eventuali dipendenze coinvolte

- Per modifiche a template HTML, CSS o JavaScript fornisci sempre il file completo aggiornato oppure applica direttamente la modifica. Evita patch parziali difficili da integrare.

- Se esiste una soluzione semplice e una complessa, proponi sempre prima quella semplice.

## Sicurezza operativa

- Non eseguire mai git commit, git push, git merge, git rebase o cancellazioni di file senza conferma esplicita.

## Qualità del codice

- Proponi sempre modifiche complete e coerenti, mai snippet parziali da incollare manualmente.
- Mantieni l'architettura Flask esistente: Blueprint, SQLAlchemy, Flask-Login, Flask-Migrate.
- Mantieni Bootstrap 5.3 e lo stile grafico esistente (tema warm brown/cream, admin.css).
- Non introdurre nuove librerie senza averle proposte e motivate prima.
- Non aggiungere commenti al codice se non strettamente necessari.

## Stack tecnico di riferimento

- Python / Flask 3.1
- SQLAlchemy + Flask-Migrate (Alembic)
- SQLite (`data/database.db`)
- Flask-Login per autenticazione admin
- Bootstrap 5.3 + Bootstrap Icons 1.11.3
- Quill.js 1.3.6 per editor rich text
- Jinja2 per i template

## Struttura del progetto

- `app.py` — entry point, seeding iniziale, context processor
- `config.py` — configurazione Flask
- `extensions.py` — init SQLAlchemy e LoginManager
- `models/` — modelli SQLAlchemy
- `routes/recipes.py` — blueprint pubblico
- `routes/admin.py` — blueprint admin
- `templates/` — template Jinja2
- `static/css/admin.css` — stile admin
- `static/uploads/recipes/` — immagini caricate
- `migrations/` — migrazioni Alembic

## Stato attuale del progetto

**Versione:** v3.0.7
**Repository:** https://github.com/wifi75/IlMioRicettario
**Branch principale:** main — pulito, allineato con origin/main
**Python:** 3.13

### Funzionalità completate
- Ricettario con calcolatore matematico (peso totale, teglie, pezzatura)
- Ingredienti master con autocomplete datalist e badge W / Farina / Liquido
- Teglie master (MasterBakeryPan) con selezione per ricetta e calcolo capacità
- Feature toggle per ricetta: pezzatura, teglie, tipo lievito, tangzhong
- Fermentazione: diretto / poolish / biga con editor prefermento Quill.js separato
- Parametri processo: temperatura chiusura, autolisi, puntata (con opzione "fino al raddoppio"), appretto
- Conversione lieviti fresco/secco: coefficiente globale + override per singola ricetta (`yeast_ratio`)
- Libreria immagini centralizzata (MasterImage): dropdown con preview dinamico, upload locale (max 2 MB)
- Wiki tecnica pubblica: editor Quill.js, slug autogenerato, 9 voci seminate all'avvio
- Setup wizard integrato: SETUP_MODE automatico se `instance/config.py` è assente o manca SECRET_KEY
- Gestione porta dal pannello admin + script CLI `set_port.py`
- Backup e ripristino: export JSON (ricette, config) e ZIP (completo con immagini)
- Tema grafico pubblico configurabile (6 temi) + titolo e descrizione sito
- Bilingue IT/EN completo: switcher bandierine in sidebar, tutti i template admin aggiornati (v3.0.7)
- Admin bloccato su smartphone (<768 px) con overlay informativo; pienamente funzionante su tablet/desktop
- Frontend pubblico ottimizzato per mobile

### Modelli SQLAlchemy
- `User` — admin con password hash
- `Recipe` — ricetta con tutti i campi e relazione ManyToMany con `MasterBakeryPan`
- `RecipeIngredient` — ingredienti della ricetta con flag farina/liquido e valore W
- `RecipeFeature` — feature toggle per ricetta (enable_piece_count, enable_pans, enable_yeast_type, enable_tangzhong, enable_baker_percentage, enable_poolish, enable_biga, enable_sourdough, enable_hydration)
- `RecipeParameter` — parametri aggiuntivi della ricetta
- `MasterIngredient` — anagrafica ingredienti globale
- `MasterBakeryPan` — anagrafica teglie globale
- `MasterImage` — libreria immagini centralizzata
- `Setting` — configurazione tema, nome sito, descrizione, conversione lieviti
- `WikiArticle` — articoli wiki con slug e categoria

### Architettura Blueprint
- `admin_bp` (`routes/admin.py`) — gestione contenuti e impostazioni
- `recipes_bp` (`routes/recipes.py`) — frontend pubblico
- `backup_bp` (`routes/backup.py`) — export/import JSON e ZIP
- `setup_bp` (`routes/setup.py`) — wizard prima configurazione (attivo solo in SETUP_MODE)

### Context processor
`inject_global_settings` (in `app.py`) inietta in tutti i template:
- `T` — dizionario traduzioni per la lingua corrente
- `current_lang` — `'it'` o `'en'`
- `settings_data` — record `Setting` attivo (tema, nome sito, ecc.)

### Deploy Linux
- systemd: `ilmioricettario.service` (file di esempio incluso nel repo)
- `instance/config.py` escluso da git: contiene solo `PORT` e `SECRET_KEY`
- Porta modificabile dal pannello admin o via `set_port.py` prima del primo avvio
- `gh` CLI non disponibile su Windows: release GitHub create manualmente via browser

### SECRET_KEY
Letta in cascata: variabile d'ambiente `SECRET_KEY` → `instance/config.py` → se assente, SETUP_MODE.
Non deve mai apparire nel codice sorgente o nel repository.

### Internazionalizzazione (v3.0.6–v3.0.7)
- `translations.py`: dizionario `{'it': {...}, 'en': {...}}` con oltre 150 chiavi
- Chiavi admin con prefisso `a_` (es. `a_cancel`, `a_rd_name`, `a_bk_export`)
- Chiavi JS iniettate come oggetto `_T` via Jinja2 nei template che hanno stringhe dinamiche
- Lingua salvata in sessione Flask via `/set-lang/<lang>`

### Debito tecnico noto
- `app.py` righe 82–87: `ALTER TABLE` raw per aggiungere colonne lievito — da sostituire con migrazione Alembic formale
- Dashboard (`templates/admin/dashboard.html`): versione e contatore moduli hardcodati (`V1`, `5`) — da rendere dinamici
- Campi `enable_hydration`, `enable_poolish`, `enable_biga`, `enable_sourdough` presenti nel modello `RecipeFeature` ma non ancora esposti nel frontend admin
- `fermentation_type` (campo nel DB e nel form) era chiamato `preferment_type` in versioni precedenti: verificare coerenza

## Cronologia decisioni

- **SQLite invece di PostgreSQL** (v1.x) — deploy standalone su server Linux senza dipendenze DB esterne. Adatto per uso monoutente/piccola community.

- **Blueprint Flask separati** — organizzazione in `admin_bp`, `recipes_bp`, `backup_bp`, `setup_bp` per separare responsabilità e semplificare la manutenzione.

- **SECRET_KEY in `instance/config.py`** (non in git) — sicurezza operativa per repository pubblico su GitHub. L'app entra in SETUP_MODE se il file è assente o la chiave è vuota.

- **Setup wizard integrato** (v3.0.1) — eliminato `installer.py` esterno su porta 5000. L'app rileva l'assenza di SECRET_KEY e reindirizza tutto su `/setup`, senza processi separati.

- **`instance/config.py`** (v3.0.0) — PORT e SECRET_KEY in un file locale mai committato, per evitare conflitti tra `git pull` e configurazione server.

- **`set_port.py`** (v3.0.2) — script CLI per impostare la porta prima del primo avvio, quando l'app non è ancora accessibile via browser.

- **Sistema bilingue con dizionario Python** invece di Flask-Babel (v3.0.6) — soluzione senza dipendenze aggiuntive. Prefisso `a_` per chiavi admin, iniettato globalmente dal context processor. Chiavi JS rese disponibili tramite oggetto `_T` Jinja2.

- **Libreria immagini centralizzata** (`MasterImage`) con gestore dropdown + preview — adottato per gestire librerie con molte foto senza confusione nella selezione (alternativa a upload diretto per-ricetta).

- **Quill.js 1.3.6 via CDN** — editor rich text per istruzioni ricette e articoli wiki, senza dipendenze Python lato server.

- **Admin bloccato su smartphone** (v2.3.2) — overlay full-screen su schermi <768 px: il pannello admin richiede tablet o computer per usabilità minima della tabella ingredienti.

- **Upsert per slug nel seeding wiki** (v3.0.4) — il seeding degli articoli wiki all'avvio usa `filter_by(slug=...)` per non duplicare voci già presenti. Evita errori dopo `db.create_all()` su database esistente.

- **`fermentation_type` come nome campo** nel form ricetta — chiamato `preferment_type` in versioni precedenti; rinominato per coerenza col modello. Da verificare che non ci siano riferimenti residui al vecchio nome.
