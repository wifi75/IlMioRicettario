# 🧫 Il Mio Ricettario - Professional Baking Suite

![Versione](https://img.shields.io/badge/version-v2.2.0-orange?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge\&logo=python)
![Framework](https://img.shields.io/badge/Framework-Flask-blue?style=for-the-badge\&logo=flask)
![Database](https://img.shields.io/badge/Database-SQLite-green?style=for-the-badge\&logo=sqlite)
![Bootstrap](https://img.shields.io/badge/UI-Bootstrap%205.3-purple?style=for-the-badge\&logo=bootstrap)

---

# 📖 Descrizione

**Il Mio Ricettario** è una piattaforma professionale dedicata alla gestione avanzata delle ricette di panificazione.

Il sistema permette di:

* archiviare formule professionali;
* gestire ingredienti centralizzati;
* monitorare idratazione e percentuali baker;
* gestire prefermenti;
* utilizzare Tangzhong;
* amministrare una libreria immagini centralizzata;
* consultare una Wiki tecnica pubblica dedicata all'arte bianca.

L'applicazione è stata progettata per essere utilizzata sia in ambiente domestico che professionale.

---

# 🚀 Novità della Versione 2.2.0

## Libreria Immagini Centralizzata

Introduzione del nuovo sistema multimediale basato sul modello:

```python
MasterImage
```

Le immagini vengono archiviate una sola volta e possono essere associate dinamicamente alle ricette.

Funzionalità:

* upload immagini centralizzato;
* anteprima immediata;
* selezione tramite menu a tendina;
* associazione persistente alle ricette;
* gestione ottimizzata di grandi librerie fotografiche.

---

## Miglioramento Backend Ricette

Nuovo sistema di selezione immagini:

* dropdown intelligente;
* anteprima dinamica;
* sincronizzazione automatica;
* mantenimento della selezione dopo il salvataggio.

---

## Stabilizzazione Interfaccia

* miglioramenti responsive;
* ottimizzazione delle card amministrative;
* pulizia dell'interfaccia;
* correzione bug di associazione immagini.

---

# 🏗️ Architettura Tecnologica

## Backend

* Python 3.13
* Flask
* Flask-SQLAlchemy
* Flask-Login

## Database

* SQLite

## Frontend

* Bootstrap 5.3
* Bootstrap Icons
* HTML5
* CSS3
* JavaScript Vanilla

## Editor

* Quill.js 1.3.6

---

# 🗄️ Struttura Principale del Database

## User

Gestione utenti amministratori.

Funzioni:

* login sicuro;
* password hashate;
* protezione Flask-Login.

---

## MasterIngredient

Anagrafica centralizzata degli ingredienti.

Campi principali:

* nome;
* forza W;
* flag farina;
* flag liquido.

---

## MasterBakeryPan

Archivio centralizzato delle teglie.

Permette l'associazione di più teglie ad una singola ricetta.

---

## MasterImage

Archivio centralizzato immagini.

Campi principali:

* filename;
* caption;
* alt_text;
* upload_date.

---

## Recipe

Archivio principale delle formule.

Include:

* descrizione;
* istruzioni;
* tempi di fermentazione;
* immagine associata;
* teglie abilitate;
* prefermenti.

---

## RecipeIngredient

Relazione ingredienti ↔ ricette.

Contiene:

* quantità;
* unità;
* metadati di calcolo;
* ordinamento.

---

## RecipeFeature

Attivazione dinamica dei moduli:

* Tangzhong;
* Poolish;
* Biga;
* gestione lieviti;
* gestione pezzature.

---

## Setting

Configurazioni globali applicazione.

---

## wiki

Archivio articoli tecnici della documentazione pubblica.

---

# 📚 Wiki Pubblica

La Wiki pubblica è accessibile tramite:

```text
/wiki
```

La sezione contiene:

* guide tecniche;
* documentazione;
* procedure operative;
* manualistica dell'arte bianca.

Il sistema è progettato per non generare errori di avvio anche in assenza della tabella database.

---

# 🧮 Funzionalità Tecniche

## Calcolo Idratazione

Calcolo automatico dell'idratazione totale.

---

## Conversione Lieviti

Supporto:

* lievito fresco;
* lievito secco.

---

## Tangzhong

Gestione automatica:

* farina dedicata;
* liquidi dedicati;
* procedura guidata.

---

## Poolish

Supporto automatico:

* idratazione 100%.

---

## Biga

Supporto automatico:

* idratazione 44%.

---

# 💻 Installazione Rapida Linux

## Clonazione

```bash
git clone https://github.com/wifi75/IlMioRicettario.git
cd IlMioRicettario
```

## Ambiente Virtuale

```bash
python3 -m venv venv
source venv/bin/activate
```

## Dipendenze

```bash
pip install -r requirements.txt
```

## Avvio

```bash
python app.py
```

---

# 🔒 Sicurezza

Il progetto utilizza:

* hashing password Werkzeug;
* autenticazione Flask-Login;
* protezione amministrativa delle rotte;
* esclusione database tramite `.gitignore`.

---

# 📁 File Esclusi da Git

```text
instance/
*.db
__pycache__/
*.pyc
```

---

# 🛣️ Roadmap Futura

## V3

* Media ponderata automatica del W.
* Gestione completa del lievito madre.
* Statistiche avanzate.
* Backup automatici.
* Import/Export ricette.

---

# 👨‍💻 Autore

Architettato e sviluppato da **Tiziano Cassone**.

© 2026 - Il Mio Ricettario
