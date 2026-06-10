# PROGETTO: Il Mio Ricettario (V2.2.0)

## PANORAMICA

* **Nome:** Il Mio Ricettario
* **Versione Architetturale:** V2.2.0
* **Stato:** Produzione Stabile
* **Repository GitHub:** https://github.com/wifi75/IlMioRicettario
* **Sviluppatore Principale:** Tiziano Cassone

---

# DESCRIZIONE

Il Mio Ricettario è una piattaforma professionale per la gestione avanzata di ricette da forno e lievitazione.

A differenza di un semplice ricettario statico, ogni formula può attivare moduli dinamici di calcolo che permettono:

* ricalcolo automatico delle grammature;
* gestione delle pezzature;
* gestione delle teglie;
* conversione dei lieviti;
* utilizzo di Tangzhong;
* gestione di Poolish e Biga;
* associazione immagini centralizzata;
* consultazione della Wiki tecnica pubblica.

---

# STACK TECNOLOGICO

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

* Quill.js v1.3.6

## Template Engine

* Jinja2

---

# ARCHITETTURA MODULARE

Ogni ricetta può attivare o disattivare funzionalità specifiche tramite il modello:

```python
RecipeFeature
```

## Modulo Pezzature

Gestione:

* numero panetti;
* peso singolo;
* peso totale impasto.

---

## Modulo Teglie

Integrazione con:

```python
MasterBakeryPan
```

Permette il calcolo automatico dell'impasto necessario in base alla capacità della teglia.

---

## Modulo Conversione Lieviti

Supporta:

* lievito fresco;
* lievito secco.

Il rapporto di conversione è configurabile globalmente.

---

## Modulo Tangzhong

Gestione automatica di:

* farina dedicata;
* liquidi dedicati;
* procedura guidata.

Parametri configurabili tramite:

```python
Setting
```

---

## Modulo Prefermentazione

Supporto per:

### Poolish

* idratazione 100%.

### Biga

* idratazione 44%.

---

## Modulo Wiki Pubblica

Rotta:

```text
/wiki
```

Sistema indipendente dal database per garantire la stabilità dell'applicazione.

---

# ARCHITETTURA DATABASE

## User

Gestione utenti amministrativi.

Funzioni:

* autenticazione;
* autorizzazione;
* password hashate.

---

## MasterIngredient

Archivio centralizzato ingredienti.

Campi principali:

* nome;
* flag farina;
* flag liquido;
* forza W.

---

## MasterBakeryPan

Archivio centralizzato:

* teglie;
* stampi;
* contenitori.

---

## MasterImage

Archivio immagini centralizzato introdotto nella v2.2.0.

Permette:

* upload unico;
* riutilizzo tra più ricette;
* gestione metadati;
* anteprima dinamica.

Campi principali:

* filename;
* caption;
* alt_text;
* upload_date.

---

## Recipe

Modello principale delle formule.

Include:

* descrizione;
* istruzioni;
* immagine associata;
* fermentazione;
* tempi tecnici;
* teglie abilitate.

---

## RecipeIngredient

Relazione ingredienti ↔ ricetta.

Contiene:

* quantità;
* unità;
* ordine;
* flag tecnici;
* forza W storicizzata.

---

## RecipeFeature

Flag booleani per attivazione moduli.

---

## Setting

Configurazione globale applicazione.

Include:

* ratio lieviti;
* parametri Tangzhong;
* nome sito;
* descrizione sito;
* tema attivo.

---

## wiki

Classe definita in:

```text
models/wiki.py
```

Mantiene volutamente il nome:

```python
wiki
```

in minuscolo.

---

# REGOLE DI SVILUPPO

## 1. File Completi

Fornire sempre file completi pronti al copia-incolla.

Sono vietati:

* placeholder;
* patch parziali;
* sezioni omesse.

---

## 2. Nessuna Query nel Context Processor

È vietato inserire query pesanti in:

```python
@app.context_processor
```

Le interrogazioni devono essere eseguite:

* nelle rotte;
* nei blueprint;
* nei servizi dedicati.

---

## 3. Stabilità Jinja

Tutti i blocchi:

```jinja2
{% if %}
{% for %}
{% block %}
```

devono essere sempre chiusi correttamente.

---

## 4. Mobile First

Interfaccia:

* responsive;
* Bootstrap nativo;
* sidebar amministrativa scura;
* contenuti su sfondo slate:

```css
#f8fafc
```

---

# LOGICHE OPERATIVE CRITICHE

## Integrazione Quill.js

Il contenuto dell'editor viene salvato tramite:

```html
<input hidden name="instructions">
```

alimentato da JavaScript.

---

## Parsing Istruzioni

Le istruzioni vengono elaborate tramite:

```python
.split('\n')
```

e renderizzate come:

* elenco numerato;
* prima parola in grassetto.

---

## Gestione Forza W

Il valore W viene:

1. letto da MasterIngredient;
2. copiato in RecipeIngredient;
3. storicizzato nella ricetta.

---

## Libreria Immagini Centralizzata

Le immagini vengono gestite tramite:

```python
MasterImage
```

e collegate tramite:

```python
Recipe.image_id
```

La selezione avviene tramite:

* dropdown;
* preview dinamica;
* associazione persistente.

---

## Rotta Wiki Pubblica

La rotta:

```text
/wiki
```

deve rimanere immune da errori dovuti a:

* assenza tabelle;
* migrazioni incomplete;
* problemi del modello wiki.

---

# FIRMA PROGETTO

Architettato e sviluppato da Tiziano Cassone.

© 2026 - Il Mio Ricettario
