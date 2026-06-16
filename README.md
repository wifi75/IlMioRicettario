# 🧫 Il Mio Ricettario - Professional Baking Suite

![Versione](https://img.shields.io/badge/version-v3.0.0-orange?style=for-the-badge)
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

Progetto sviluppato da Tiziano Cassone

---

# 🚀 Novità

## v3.0.0

### Web Installer

* Wizard di installazione accessibile via browser (`python installer.py` → http://server:5000)
* Generazione automatica di `instance/config.py` con PORT e SECRET_KEY
* Se avviato come root: crea, abilita e avvia il servizio systemd in automatico
* Mostra il file `.service` pronto da copiare con un click

### Configurazione Istanza

* Porta e SECRET_KEY configurabili in `instance/config.py` (mai in git)
* `git pull` non genera mai più conflitti sulla porta
* La variabile d'ambiente ha sempre priorità sul file istanza

### Backup e Ripristino

* Export ricette (JSON), configurazione (JSON), backup completo con immagini (ZIP)
* Import con modalità Merge (aggiunge) o Replace (ripristino completo)
* Accessibile da Admin → Manutenzione → Backup e Ripristino

### Pannello Admin Riorganizzato

* Sidebar suddivisa in quattro sezioni: Catalogo, Sistema, Account, Manutenzione
* Aggiunta voce Conversione Lieviti (route `/admin/settings/yeast` prima mancante)
* Aggiunta sezione Manutenzione con Backup e Ripristino

---

## v2.3.2

### Mobile Responsive

* Tabella formula con 3 colonne ottimizzate su smartphone: Materia Prima, (W), Grammi
* Intestazioni tabella abbreviate su mobile, senza testo a capo
* Admin panel bloccato su smartphone con overlay e messaggio esplicativo
* Wiki tecnica pre-popolata con 9 voci al primo avvio

---

## v2.3.1

### Mobile Responsive

* Tabella ingredienti ridotta a 2 colonne su smartphone (Materia Prima + Grammi)
* Eliminato scroll orizzontale nella pagina ricetta su mobile
* Pulsanti teglie con area di tocco minima 44 × 44 px
* Prevenzione zoom automatico iOS su input e select
* Hero image ricetta espansa a larghezza intera su smartphone
* Line-height istruzioni ottimizzato per la lettura su piccoli schermi

---

## v2.3.0

### Sicurezza

* SECRET_KEY rimossa dal codice sorgente: letta da variabile d'ambiente
* Password admin di default eliminata: generata randomicamente alla prima installazione
* L'applicazione non si avvia se SECRET_KEY non è impostata

### Mobile Responsive

* Pulsante hamburger per la sidebar admin su smartphone e tablet
* Overlay scuro con chiusura al tocco
* Titoli e padding ottimizzati nella scheda ricetta pubblica su mobile
* Tab procedimento scorrevoli orizzontalmente su smartphone
* Tabella ingredienti correttamente scrollabile su mobile

### Correzioni

* Allineamento newline POSIX in tutti i file modificati

---

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

## 1 — Clonazione Repository

```bash
cd /var/www
git clone https://github.com/wifi75/IlMioRicettario.git
cd IlMioRicettario
```

---

## 2 — Ambiente Virtuale e Dipendenze

```bash
apt update && apt install python3 python3-venv python3-pip -y
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 3 — Installazione Guidata via Browser (Web Installer)

Avvia il wizard di installazione:

```bash
sudo python installer.py
```

Apri il browser su:

```text
http://<indirizzo-server>:5000
```

Il wizard chiede:

* **Porta** dell'applicazione (es. 8100)
* **Secret Key** (generata automaticamente con un click)

Al termine genera `instance/config.py` con PORT e SECRET_KEY.
Se avviato con `sudo`, crea e abilita il servizio systemd in automatico.

> `instance/config.py` non è mai incluso in git: `git pull` non genererà mai conflitti sulla porta o sulla chiave.

---

## 4 — Se il servizio NON è stato abilitato automaticamente

Copia il contenuto mostrato nella pagina di successo dell'installer e salvalo in:

```bash
nano /etc/systemd/system/ilmioricettario.service
```

Poi abilita e avvia:

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
systemctl restart ilmioricettario
```

> Nessun conflitto sulla porta: la configurazione è in `instance/config.py`, mai in git.

Aggiornare le dipendenze solo se `requirements.txt` è cambiato:

```bash
source venv/bin/activate
pip install -r requirements.txt
```

---

## Log

```bash
journalctl -u ilmioricettario -f
journalctl -u ilmioricettario -n 100 --no-pager
journalctl -xeu ilmioricettario
```

---

# 🔒 Sicurezza

Il progetto utilizza:

* Hashing password Werkzeug (bcrypt)
* Autenticazione Flask-Login
* Protezione amministrativa delle rotte
* Gestione utenti sicura
* SECRET_KEY configurabile via `instance/config.py` o variabile d'ambiente (mai hardcoded)
* Password admin generata randomicamente alla prima installazione

> La SECRET_KEY firma i cookie di sessione Flask ed è completamente separata dalla password amministratore.
>
> La variabile d'ambiente ha priorità su `instance/config.py`. L'applicazione non si avvia se SECRET_KEY non è configurata in nessuno dei due posti.

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

## V3.x

* Media ponderata automatica del W delle farine
* Gestione completa del lievito madre
* Statistiche avanzate di utilizzo ricette
* Backup automatici schedulati
* API REST pubbliche
* Multi-utente con ruoli

---

# 👨‍💻 Autore

Architettato e sviluppato da **Tiziano Cassone**

© 2026 - Il Mio Ricettario