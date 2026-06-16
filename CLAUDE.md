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

**Versione:** v3.0.6

### Funzionalità implementate
- Ricettario dinamico con calcolatore matematico (peso totale, teglie, pezzatura)
- Pannello admin completo con Flask-Login (ricette, ingredienti, teglie, wiki, backup)
- Ingredienti master con autocomplete datalist e badge W/Farina/Liquido
- Teglie master con selezione per ricetta e calcolo capacità
- Wiki tecnica con editor Quill.js e slug autogenerato
- Setup wizard integrato: SETUP_MODE automatico se `instance/config.py` è assente o manca SECRET_KEY
- Gestione porta applicazione via pannello admin (`set_port.py` + `instance/config.py`)
- Backup e ripristino dati in formato JSON (ricette, config) e ZIP (completo con immagini)
- Gestore immagini: dropdown con preview dinamico e upload locale (max 2 MB)
- Sistema bilingue IT/EN con switcher bandierine in sidebar admin (v3.0.6)
- Tema grafico pubblico configurabile (6 temi) da pannello admin
- Conversione lieviti fresco/secco configurabile da pannello admin
- Responsive mobile: admin bloccato su tablet/desktop, frontend pubblico ottimizzato

### Architettura Blueprint
- `admin_bp` (`routes/admin.py`) — gestione contenuti e impostazioni
- `recipes_bp` (`routes/recipes.py`) — frontend pubblico
- `backup_bp` (`routes/backup.py`) — export/import JSON e ZIP
- `setup_bp` (`routes/setup.py`) — wizard prima configurazione

### Deploy
- Linux con systemd (`ilmioricettario.service`)
- `instance/config.py` escluso da git: contiene solo `PORT` e `SECRET_KEY`
- Porta configurabile dal pannello admin (script `set_port.py`)
- `gh` CLI non disponibile su Windows: release GitHub create manualmente

### Internazionalizzazione (v3.0.6)
- `translations.py`: dizionario Python `{'it': {...}, 'en': {...}}`
- Context processor in `app.py`: inietta `T` e `current_lang` in tutti i template
- Chiavi admin con prefisso `a_` (es. `a_cancel`, `a_rd_name`)
- Chiavi JS iniettate come oggetto `_T` via Jinja2 nei template che le usano
- Lingua salvata in sessione Flask via `/set-lang/<lang>`

## Cronologia decisioni

- **SQLite invece di PostgreSQL** — deploy standalone su server Linux senza dipendenze DB esterne. Adatto per uso monoutente/piccola community.

- **Blueprint Flask separati** — organizzazione in `admin_bp`, `recipes_bp`, `backup_bp`, `setup_bp` per separare responsabilità e semplificare la manutenzione.

- **SECRET_KEY in `instance/config.py`** (non in git) — sicurezza operativa per repository pubblico su GitHub. L'app entra in SETUP_MODE se il file è assente.

- **Sistema bilingue con dizionario Python** invece di Flask-Babel — soluzione senza dipendenze aggiuntive, con prefisso `a_` per chiavi admin, iniettato globalmente dal context processor.

- **Quill.js 1.3.6 via CDN** — editor rich text per istruzioni ricette e articoli wiki, senza dipendenze Python lato server.

- **Setup wizard integrato** (v3.0.1) — eliminato installer esterno. Se SECRET_KEY manca in `instance/config.py`, l'app avvia automaticamente in SETUP_MODE.

- **Gestore immagini con dropdown + preview** — adottato per gestire librerie con molte immagini senza confusione nella selezione.

- **`fermentation_type` come nome campo** nel form ricetta (vs `preferment_type` in recipe_detail) — eredità storica: i due template usano nomi diversi per lo stesso concetto. Da unificare in futuro.
