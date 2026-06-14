# 🧫 Il Mio Ricettario - Professional Baking Suite

![Versione](https://img.shields.io/badge/version-v2.2.3-orange?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge&logo=python)
![Framework](https://img.shields.io/badge/Framework-Flask-blue?style=for-the-badge&logo=flask)
![Database](https://img.shields.io/badge/Database-SQLite-green?style=for-the-badge&logo=sqlite)
![Bootstrap](https://img.shields.io/badge/UI-Bootstrap%205.3-purple?style=for-the-badge&logo=bootstrap)

---

# 📖 Descrizione

**Il Mio Ricettario** è una piattaforma professionale dedicata alla gestione avanzata delle ricette di panificazione.

Il sistema permette di:

* Archiviare formule professionali
* Gestire ingredienti centralizzati
* Monitorare idratazione e percentuali baker
* Gestire prefermenti
* Utilizzare Tangzhong
* Amministrare una libreria immagini centralizzata
* Consultare una Wiki tecnica pubblica dedicata all'arte bianca

L'applicazione è stata progettata per essere utilizzata sia in ambiente domestico che professionale.

Repository ufficiale:

https://github.com/wifi75/IlMioRicettario

---

# 📄 Licenza

Progetto sviluppato da Tiziano Cassone.

Tutti i diritti riservati.

---

# 🚀 Novità della Serie 2.2

## v2.2.3

### Calcolatore Ricette

* Corretto il peso iniziale delle ricette
* Il frontend utilizza ora il peso reale della formula
* Eliminata l'influenza delle vecchie impostazioni memorizzate nel browser

### Gestione Cache

* Nuovo sistema Local Storage versionato
* Compatibilità migliorata dopo gli aggiornamenti
* Eliminati problemi causati da cache obsolete

### Editor Procedure

* Migliorata la pulizia del contenuto incollato da siti esterni
* Gestione più robusta di HTML, emoji e contenuti provenienti dai social network
* Procedure più leggere e compatibili con il frontend

---

## Libreria Immagini Centralizzata

Introduzione del nuovo sistema multimediale basato sul modello:

```python
MasterImage
```

Le immagini vengono archiviate una sola volta e possono essere associate dinamicamente alle ricette.

### Funzionalità

* Upload immagini centralizzato
* Anteprima immediata
* Selezione tramite menu a tendina
* Associazione persistente alle ricette
* Gestione ottimizzata di grandi librerie fotografiche

---

# 🏗️ Architettura Tecnologica

## Backend

* Python 3.13
* Flask
* Flask-SQLAlchemy
* Flask-Login
* Flask-Migrate

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

## Template Engine

* Jinja2

---

# 🗄️ Struttura Principale del Database

## User

Gestione utenti amministratori.

* Login sicuro
* Password hashate
* Protezione Flask-Login

---

## MasterIngredient

Anagrafica centralizzata degli ingredienti.

* Nome
* Forza W
* Flag farina
* Flag liquido

---

## MasterBakeryPan

Archivio centralizzato delle teglie.

Permette l'associazione di più teglie ad una singola ricetta.

---

## MasterImage

Archivio centralizzato immagini.

* Filename
* Caption
* Alt Text
* Upload Date

---

## Recipe

Archivio principale delle formule.

* Descrizione
* Istruzioni
* Immagine associata
* Image ID
* Tempi di fermentazione
* Teglie abilitate
* Prefermenti

---

## RecipeIngredient

Relazione ingredienti ↔ ricette.

* Quantità
* Unità
* Metadati di calcolo
* Ordinamento
* Valore W storicizzato

---

## RecipeFeature

Attivazione dinamica dei moduli:

* Tangzhong
* Poolish
* Biga
* Gestione lieviti
* Gestione pezzature

---

## Setting

Configurazioni globali applicazione.

---

## Wiki

Archivio articoli tecnici della documentazione pubblica.

---

# 📚 Wiki Pubblica

La Wiki pubblica è accessibile tramite:

```text
/wiki
```

Contiene:

* Guide tecniche
* Documentazione
* Procedure operative
* Manualistica dell'arte bianca

---

# 🧮 Funzionalità Tecniche

## Calcolo Idratazione

Calcolo automatico dell'idratazione totale.

## Conversione Lieviti

Supporto:

* Lievito fresco
* Lievito secco

## Tangzhong

Gestione automatica:

* Farina dedicata
* Liquidi dedicati
* Procedura guidata

## Poolish

Supporto automatico:

* Idratazione 100%

## Biga

Supporto automatico:

* Idratazione 44%

---

# 💻 Installazione Produzione Linux

## Clonazione Repository

```bash
cd /var/www

git clone https://github.com/wifi75/IlMioRicettario.git

cd IlMioRicettario
```

---

## Creazione Ambiente Virtuale

```bash
apt update

apt install python3 python3-venv python3-pip -y

python3 -m venv venv

source venv/bin/activate
```

---

## Installazione Dipendenze

```bash
pip install -r requirements.txt
```

---

## Cartelle Automatiche

Al primo avvio vengono create automaticamente:

```text
data/
static/uploads/
static/uploads/recipes/
```

Non è necessario creare manualmente alcuna cartella.

> L'applicazione crea automaticamente le cartelle necessarie al primo avvio.
>
> Se il database SQLite è già presente sul sistema, non è richiesta alcuna inizializzazione manuale.

---

## Avvio Applicazione

```bash
python app.py
```

Configurazione predefinita:

```text
Host: 0.0.0.0
Porta: 8100
```

---

# ⚙️ Installazione come Servizio Systemd

Creare:

```bash
nano /etc/systemd/system/ilmioricettario.service
```

Contenuto:

```ini
[Unit]
Description=Il Mio Ricettario Flask
After=network.target

[Service]
User=root
Group=root

WorkingDirectory=/var/www/IlMioRicettario

Environment="PATH=/var/www/IlMioRicettario/venv/bin"

ExecStart=/var/www/IlMioRicettario/venv/bin/python /var/www/IlMioRicettario/app.py

Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

---

## Attivazione Servizio

```bash
systemctl daemon-reload

systemctl enable ilmioricettario

systemctl start ilmioricettario
```

Verifica:

```bash
systemctl status ilmioricettario
```

---

## Aggiornamento Applicazione

```bash
cd /var/www/IlMioRicettario

git pull origin main
```

Aggiornare le dipendenze:

```bash
source venv/bin/activate

pip install -r requirements.txt
```

Riavviare:

```bash
systemctl restart ilmioricettario
```

---

## Log

Visualizzazione continua:

```bash
journalctl -u ilmioricettario -f
```

Ultimi 100 eventi:

```bash
journalctl -u ilmioricettario -n 100 --no-pager
```

Errori:

```bash
journalctl -xeu ilmioricettario
```

---

# 🔒 Sicurezza

Il progetto utilizza:

* Hashing password Werkzeug
* Autenticazione Flask-Login
* Protezione amministrativa delle rotte
* Gestione utenti sicura

---

# 📁 File Esclusi da Git

```text
data/database.db
data/*.db
data/*.sqlite

instance/

__pycache__/
*.pyc
*.pyo
*.pyd

.env
```

---

# 🛣️ Roadmap Futura

## V3

* Media ponderata automatica del W
* Gestione completa del lievito madre
* Statistiche avanzate
* Backup automatici
* Import/Export ricette
* API REST pubbliche

---

# 👨‍💻 Autore

Architettato e sviluppato da **Tiziano Cassone**

© 2026 - Il Mio Ricettario