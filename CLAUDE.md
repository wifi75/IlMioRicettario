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
