# PROGETTO: Il Mio Ricettario (V3.0.0)

## PANORAMICA

* **Nome:** Il Mio Ricettario
* **Versione Architetturale:** V3.0.0
* **Stato:** Produzione Stabile
* **Repository GitHub:** https://github.com/wifi75/IlMioRicettario
* **Sviluppatore Principale:** Tiziano Cassone

---

# DESCRIZIONE

Il Mio Ricettario è una piattaforma professionale per la gestione avanzata di ricette di panificazione, lievitazione e arte bianca.

A differenza di un semplice archivio statico, ogni ricetta può attivare moduli dinamici che consentono:

* ricalcolo automatico delle grammature;
* gestione pezzature;
* gestione teglie;
* conversione lieviti;
* gestione Tangzhong;
* gestione Poolish;
* gestione Biga;
* libreria immagini centralizzata;
* Wiki tecnica pubblica;
* calcolo dinamico del peso impasto;
* frontend responsive per consultazione pubblica.

---

# STACK TECNOLOGICO

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

# ARCHITETTURA GENERALE

## Area Pubblica

Permette la consultazione delle ricette pubblicate.

Funzionalità:

* visualizzazione ricette;
* visualizzazione immagini;
* calcolo ingredienti;
* gestione pezzature;
* gestione teglie;
* consultazione Wiki.

## Area Amministrativa

Protetta tramite Flask-Login.

Funzionalità:

* gestione ricette;
* gestione ingredienti;
* gestione immagini;
* gestione teglie;
* gestione impostazioni;
* gestione Wiki.

---

# ARCHITETTURA MODULARE

Ogni ricetta può attivare o disattivare moduli specifici tramite il modello:

```python
RecipeFeature
```

## Modulo Pezzature

Gestisce:

* numero panetti;
* peso singolo;
* peso totale impasto.

## Modulo Teglie

Basato sul modello:

```python
MasterBakeryPan
```

Permette il calcolo automatico della quantità di impasto necessaria.

## Modulo Conversione Lieviti

Supporta:

* lievito fresco;
* lievito secco.

Rapporto configurabile tramite Setting.

## Modulo Tangzhong

Gestione automatica di:

* farina dedicata;
* liquidi dedicati;
* percentuali configurabili.

## Modulo Prefermentazione

### Poolish

* idratazione 100%.

### Biga

* idratazione 44%.

---

# ARCHITETTURA DATABASE

## User

Gestione utenti amministrativi.

Funzioni:

* autenticazione;
* autorizzazione;
* password hashate.

## MasterIngredient

Archivio ingredienti centralizzato.

Campi principali:

* nome;
* forza W;
* flag farina;
* flag liquido.

## MasterBakeryPan

Archivio teglie e stampi.

## MasterImage

Archivio immagini centralizzato.

Campi:

* filename;
* caption;
* alt_text;
* upload_date.

## Recipe

Modello principale.

Contiene:

* descrizione;
* istruzioni;
* immagine;
* fermentazione;
* tempi tecnici;
* prefermenti;
* teglie abilitate.

## RecipeIngredient

Relazione ingredienti ↔ ricetta.

Contiene:

* quantità;
* unità;
* ordine;
* valore W storicizzato.

## RecipeFeature

Attivazione dinamica dei moduli.

## Setting

Configurazioni globali.

## Wiki

Documentazione pubblica.

---

# GESTIONE ISTRUZIONI

## Quill.js

Le istruzioni vengono salvate come HTML generato da Quill.js.

Durante il salvataggio il sistema esegue una sanificazione del contenuto per eliminare:

* immagini emoji esterne;
* attributi HTML indesiderati;
* markup proveniente da Facebook;
* codice HTML superfluo.

Il frontend renderizza direttamente l'HTML sanificato.

---

# CALCOLATORE DINAMICO FRONTEND

Il frontend pubblico consente:

* ridimensionamento ingredienti;
* calcolo peso impasto;
* calcolo pezzature;
* calcolo teglie;
* conversione lievito.

## Regola Fondamentale

Il peso iniziale deve sempre essere il peso reale della ricetta.

Il browser non deve alterare automaticamente la formula originale.

---

# GESTIONE CACHE FRONTEND

Le preferenze vengono memorizzate tramite Local Storage versionato.

Possono essere salvati:

* modalità di calcolo;
* preferenze utente;
* impostazioni frontend.

Non deve essere memorizzato il peso iniziale della ricetta.

---

# LIBRERIA IMMAGINI CENTRALIZZATA

Le immagini vengono gestite tramite:

```python
MasterImage
```

e collegate tramite:

```python
Recipe.image_id
```

Funzionalità:

* upload centralizzato;
* riutilizzo tra ricette;
* preview dinamica;
* associazione persistente.

---

# WIKI PUBBLICA

Rotta:

```text
/wiki
```

La Wiki deve restare indipendente da eventuali errori delle altre sezioni.

---

# REGOLE DI SVILUPPO

## 1. File Completi

Fornire sempre file completi pronti al copia-incolla.

Vietati:

* placeholder;
* patch parziali;
* sezioni omesse.

## 2. Nessuna Query nel Context Processor

Non inserire query pesanti in:

```python
@app.context_processor
```

Le query devono essere eseguite:

* nelle rotte;
* nei servizi;
* nei blueprint.

## 3. Stabilità Jinja

Tutti i blocchi devono essere chiusi correttamente:

```jinja2
{% if %}
{% for %}
{% block %}
```

## 4. Mobile First

Interfaccia:

* responsive;
* Bootstrap nativo;
* sidebar amministrativa scura con hamburger menu su mobile;
* overlay scuro al tocco per chiudere la sidebar;
* area pubblica ottimizzata per smartphone;
* layout ottimizzato mobile.

## 5. Sicurezza Configurazione

La `SECRET_KEY` deve essere sempre letta da variabile d'ambiente.

Non deve mai essere hardcoded nel sorgente.

Comando per generare una chiave sicura:

```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

La `SECRET_KEY` firma i cookie di sessione Flask ed è indipendente dalla password amministratore.

## 6. Database Mai Versionato

Il database SQLite non deve essere pubblicato nel repository Git.

File da escludere:

```text
data/database.db
data/*.db
data/*.sqlite
```

Il database deve esistere esclusivamente nei sistemi locali o di produzione.

---

# DEPLOY PRODUZIONE

## Installazione Guidata (Web Installer)

```bash
sudo python installer.py
# → apri http://<server>:5000
```

Il wizard genera `instance/config.py` con PORT e SECRET_KEY e,
se avviato come root, crea e abilita il servizio systemd in automatico.

## Configurazione Istanza

La porta e la SECRET_KEY vengono lette da `instance/config.py`:

```python
SECRET_KEY = "..."
PORT = 8100
```

Questo file non è mai in git. La variabile d'ambiente `SECRET_KEY` ha priorità su `instance/config.py`.

## Aggiornamento

```bash
git pull origin main
systemctl restart ilmioricettario
```

Nessun conflitto: `instance/config.py` non viene mai sovrascritto da git.

## Comandi Systemd

```bash
systemctl start ilmioricettario
systemctl stop ilmioricettario
systemctl restart ilmioricettario
systemctl status ilmioricettario
journalctl -u ilmioricettario -f
```

---

# ROADMAP V3.x

* media ponderata automatica del W delle farine;
* gestione completa lievito madre;
* statistiche avanzate di utilizzo ricette;
* backup automatici schedulati;
* API REST pubbliche;
* multi-utente con ruoli.

---

# FIRMA PROGETTO

Architettato e sviluppato da Tiziano Cassone.

© 2026 - Il Mio Ricettario
