## v3.0.7 - 2026-06-16

### Aggiunto

* **Footer Versione e Link GitHub:** Il footer del sito pubblico mostra ora la versione dell'applicazione (letta da `config.py` via context processor) e un link al repository GitHub con icona Bootstrap Icons.

* **Bilingue IT/EN Completo — Tutti i Template Admin:** Completamento del supporto bilingue su tutti i template del pannello admin: `backup.html`, `wiki_list.html`, `wiki_form.html`, `recipe_form.html`, `recipe_detail.html`, `recipes.html`, `dashboard.html`, `ingredients_master.html`, `pans_master.html`, `settings_theme.html`, `settings_yeast.html`, `settings_port.html`, `change_password.html`.

* **`config.py` — Costante `APP_VERSION`:** Aggiunta la costante `APP_VERSION = 'v3.0.7'` in `Config`, iniettata globalmente dal context processor come `app_version`.

* **`AGENTS.md` — Documentazione Interna Espansa:** Aggiunte e ampliate le sezioni _Stato attuale del progetto_ (con modelli, context processor, debito tecnico) e _Cronologia decisioni_.

---

## v3.0.6 - 2026-06-16

### Aggiunto

* **Sistema Bilingue IT/EN (`translations.py`):** Introdotto il dizionario di traduzioni con oltre 150 chiavi organizzate per sezione (sidebar, admin condivisi, statistiche, dashboard, lista ricette, form ricetta, ingredienti, teglie, tema, lieviti, porta, password, backup, wiki). Il pannello admin e il frontend pubblico sono disponibili in italiano e in inglese.

* **Switcher Lingua con Bandierine:** Pulsanti 🇮🇹 / 🇬🇧 nella sidebar admin e nel footer pubblico per cambiare lingua a runtime. La preferenza viene salvata nella sessione Flask via `/set-lang/<lang>`.

* **Context Processor Globalizzato:** Le chiavi `T`, `current_lang` e `settings_data` sono ora disponibili in tutti i template senza passaggi espliciti nelle singole rotte.

* **Template Pubblici Aggiornati:** `recipes_list.html`, `recipe_public_detail.html`, `wiki_public.html` aggiornati con `{{ T.* }}` per tutte le stringhe statiche visibili all'utente. Le stringhe dinamiche JS sono iniettate via oggetto `_T` Jinja2.

---

## v3.0.5 - 2026-06-16

### Modificato

* **Titoli Pagina Admin Coerenti con Sidebar:** I titoli `{% block title %}` e `{% block page_title %}` di tutti i template admin sono ora allineati alle voci della sidebar, eliminando discrepanze tra voce di menu, intestazione pagina e titolo del browser.

---

## v3.0.4 - 2026-06-16

### Corretto

* **Wiki — Seeding Upsert per Slug:** Il seeding degli articoli wiki all'avvio usa ora `filter_by(slug=...)` per evitare la duplicazione delle voci su database già esistenti. Il primo avvio su un database vuoto popola correttamente i 9 articoli tecnici dell'arte bianca.

* **Fix Stile Editor Quill — Wiki Admin:** Corretti i bordi e il padding dell'editor Quill nella pagina di creazione e modifica articoli wiki. Il tema `snow` è ora applicato correttamente.

---

## v3.0.3 - 2026-06-16

### Aggiunto

* **Modifica Articoli Wiki dall'Admin (`/admin/wiki/<id>/edit`):** Aggiunta la route e il template per la modifica degli articoli wiki esistenti. In precedenza era possibile solo creare nuovi articoli.

* **Editor Quill.js per Articoli Wiki:** L'editor rich text Quill.js è ora disponibile nel form di creazione e modifica degli articoli wiki, con barra degli strumenti identica a quella usata per le istruzioni delle ricette (grassetto, corsivo, sottolineato, intestazioni H2/H3, liste).

* **Slug Autogenerato nel Form Wiki:** Il campo slug viene generato automaticamente in JavaScript dal titolo durante la creazione. In modifica rimane bloccato per non invalidare i link esistenti.

---

## v3.0.2 - 2026-06-16

### Aggiunto

* **Gestione Porta dal Pannello Admin (`/admin/settings/port`):** Nuova pagina nella sezione Sistema che permette di modificare la porta di ascolto dell'applicazione direttamente dal browser. Il salvataggio aggiorna `instance/config.py` preservando la SECRET_KEY esistente. La pagina mostra il comando `systemctl restart` con pulsante copia.

* **Script `set_port.py`:** Script interattivo da riga di comando per impostare la porta prima del primo avvio, quando la porta 8080 è già occupata da un altro servizio. Crea `instance/config.py` con solo PORT — l'app entra comunque in SETUP_MODE sulla porta configurata, senza richiedere variabili d'ambiente o modifiche al file `.service`.

* **`INSTALL.md` — Guida Installazione Dedicata:** Nuovo file con guida step-by-step in 10 passi per l'installazione su server Linux. Tutti i comandi sono evidenziati e pronti per il copia-incolla. Include sezione risoluzione problemi, gestione post-installazione e reset configurazione.

---

## v3.0.1 - 2026-06-16

### Aggiunto

* **Setup Wizard Integrato (`/setup`):** Sostituisce l'installer esterno `installer.py` (porta 5000). L'app rileva l'assenza di `instance/config.py` e entra in SETUP_MODE, reindirizzando tutte le rotte su `/setup`. Il wizard raccoglie porta e Secret Key, scrive `instance/config.py` e mostra le istruzioni per il riavvio.

* **`ilmioricettario.service.example`:** Template del file systemd incluso nel repository, pronto da copiare in `/etc/systemd/system/`. Non contiene SECRET_KEY (gestita da `instance/config.py`).

### Rimosso

* **`installer.py` e `templates/installer/`:** Rimosso il wizard esterno su porta 5000, sostituito dal setup integrato.

---

## v3.0.0 - 2026-06-16

### Aggiunto

* **Web Installer (`installer.py`):** Wizard di installazione guidata accessibile via browser su porta 5000. Genera automaticamente `instance/config.py` con PORT e SECRET_KEY. Se avviato come root crea, abilita e avvia il servizio systemd in automatico. Altrimenti mostra il file `.service` pronto da copiare con un click.

* **`instance/config.py` — Configurazione Istanza Server:** La porta dell'applicazione e la SECRET_KEY possono ora essere definite in `instance/config.py`, file locale mai incluso in git. Elimina i conflitti tra `git pull` e modifiche locali alla porta. La variabile d'ambiente `SECRET_KEY` ha priorità su `instance/config.py`.

* **Sistema Backup e Ripristino (`/admin/backup`):** Export e import completo di ricette, configurazione e immagini. Tre modalità di export: Ricette (JSON), Configurazione (JSON), Backup Completo (ZIP con immagini incluse). Import con due modalità: Merge (aggiunge senza sovrascrivere) e Replace (ripristino completo).

* **Route Conversione Lieviti (`/admin/settings/yeast`):** Aggiunta la route mancante per il template `settings_yeast.html`. Il rapporto di conversione fresco/secco è ora accessibile dal menu admin.

* **Riorganizzazione Sidebar Admin:** Il menu laterale è suddiviso in quattro sezioni tematiche — Catalogo, Sistema, Account, Manutenzione — per una navigazione più chiara e professionale.

---

## v2.3.2 - 2026-06-16

### Modificato e Corretto

* **Layout Tabella Formula su Mobile:** Intestazioni con `white-space: nowrap` per evitare il testo a capo. Header "Forza (W)" abbreviato in "(W)" su smartphone, "Grammi Necessari" abbreviato in "Grammi". Larghezze colonne ottimizzate tramite classi `col-w` (20%) e `col-grammi` (33%).

* **Riga TOTAL IMPASTO:** Corretto `colspan` a 2 con cella vuota hidden per la colonna Percentuale Baker, garantendo rendering corretto su tutti i breakpoint.

* **Admin Panel Bloccato su Smartphone:** Overlay full-screen su schermi < 768 px che informa l'utente che il pannello richiede tablet o computer, con link diretto al sito pubblico. Admin pienamente funzionante su tablet e desktop.

* **Wiki Tecnica — 9 Voci Seminate:** Aggiunte al database all'avvio (solo se la wiki è vuota) le voci che documentano il funzionamento del calcolatore, le tecniche di panificazione (Tangzhong, Biga, Poolish, percentuale baker, idratazione, valore W) e le guide operative (pezzature, teglie, conversione lieviti).

---

## v2.3.1 - 2026-06-16

### Modificato e Corretto

* **Tabella Ingredienti Mobile — Layout a 2 Colonne:** Su smartphone (< 768 px) la tabella ingredienti mostra ora sole due colonne — Materia Prima e Grammi Necessari — eliminando lo scroll orizzontale e la troncatura del testo. Le colonne Forza (W) e Percentuale Baker restano visibili su tablet e desktop.

* **Fix Overflow Orizzontale Pagina Ricetta:** Rimosso il doppio nesting del container Bootstrap nella pagina dettaglio ricetta. L'involucro esterno era già fornito da `base.html`; il secondo `container py-4` interno causava un doppio padding laterale che riduceva la larghezza utile di 24 px e generava overflow su schermi da 375 px.

* **Pulsanti Teglie con Area di Tocco 44 px:** I pulsanti `−` e `+` per la gestione delle teglie rispettano ora il minimo touch target di 44 × 44 px raccomandato da Apple e Google.

* **Prevenzione Zoom Automatico iOS:** Gli `input[type="number"]` e i `select` hanno ora `font-size: 16px` su mobile, soglia minima richiesta da Safari per non attivare lo zoom automatico della pagina al tocco.

* **Hero Image Ricetta Espansa su Mobile:** Corretti i conflitti `!important` che impedivano al media query mobile di ridimensionare correttamente l'immagine di testa della ricetta. Su smartphone l'immagine occupa ora la larghezza intera disponibile.

* **Riduzione Line-Height Istruzioni su Mobile:** Il testo delle istruzioni passa da `line-height: 2` a `line-height: 1.65` su mobile, riducendo lo scroll verticale mantenendo la leggibilità.

---

## v2.3.0 - 2026-06-16

### Aggiunto

* **Sidebar Amministrativa Responsive:** Introdotto il pulsante hamburger per aprire e chiudere il menu laterale admin su smartphone e tablet. La sidebar si nasconde automaticamente su schermi con larghezza inferiore a 992 px e scorre dal bordo sinistro con animazione fluida.

* **Overlay Mobile Sidebar:** Aggiunto uno strato scuro semitrasparente che oscura il contenuto quando la sidebar è aperta su mobile, con chiusura al tocco.

* **Ottimizzazione Leggibilità Ricette su Mobile:** Ridimensionati i titoli H1, ridotti i padding interni delle card e resi i tab del procedimento scorrevoli orizzontalmente su smartphone, con scrollbar nascosta per un aspetto pulito.

* **Tabella Ingredienti Scorrevole in Amministrazione:** La tabella ingredienti nel form di modifica ricetta attiva correttamente lo scroll orizzontale su dispositivi mobili tramite `min-width: 580px`.

* **Password Admin Randomizzata alla Prima Installazione:** Il sistema genera automaticamente una password sicura a 16 caratteri alla prima installazione e la mostra via console. Non esistono più credenziali default nel codice sorgente.

---

### Modificato e Corretto

* **SECRET_KEY Sicura:** Rimossa la chiave segreta hardcoded da `config.py`. La `SECRET_KEY` viene ora letta esclusivamente dalla variabile d'ambiente omonima. L'applicazione si rifiuta di avviarsi con un `RuntimeError` esplicito se la variabile non è impostata.

* **Allineamento Newline POSIX:** Aggiunti i caratteri di fine riga mancanti in `app.py`, `static/css/admin.css`, `templates/base.html`, `templates/recipe_public_detail.html`.

* **Configurazione Systemd:** Il servizio deve ora includere la voce `Environment="SECRET_KEY=..."` nella sezione `[Service]`.

---

### Note Tecniche

* Nessuna nuova dipendenza Python introdotta.

* La `SECRET_KEY` firma i cookie di sessione Flask (HMAC) ed è completamente separata dalla password dell'utente amministratore.

* La password admin è sempre salvata come hash bcrypt nella tabella `users` — la `SECRET_KEY` non la riguarda.

* Tecnologia hamburger: CSS `transform: translateX(-100%)` + JavaScript vanilla IIFE, senza nuove librerie.

---

## v2.2.0 - 2026-06-10

### Aggiunto

* **Libreria Immagini Centralizzata (`MasterImage`):** Introdotto il nuovo modello SQLAlchemy dedicato alla gestione centralizzata delle immagini delle ricette. Le immagini vengono archiviate una sola volta e possono essere associate dinamicamente a più formule.

* **Sistema di Associazione Immagini alle Ricette:** Aggiunta la colonna `image_id` al modello `Recipe` per consentire il collegamento diretto con il catalogo immagini centralizzato.

* **Selettore Immagini Intelligente:** Implementato un sistema basato su menu a tendina per la scelta delle immagini dal backend, progettato per gestire librerie fotografiche di grandi dimensioni senza sovraccaricare l'interfaccia.

* **Anteprima Dinamica Immagini:** Inserito un motore JavaScript che aggiorna l'anteprima in tempo reale durante la selezione dell'immagine.

* **Archivio Multimediale Riutilizzabile:** Le immagini caricate possono essere riutilizzate da più ricette senza generare duplicazioni inutili dei file sul filesystem.

---

### Modificato e Corretto

* **Persistenza Associazione Immagine:** Corretta la sincronizzazione tra form amministrativo, database SQLite e rendering frontend. Le immagini associate rimangono correttamente selezionate anche dopo il salvataggio e la riapertura della scheda ricetta.

* **Correzione Rendering Backend:** Risolto il problema che impediva la visualizzazione dell'anteprima immagine durante la modifica di una ricetta già esistente.

* **Ottimizzazione Interfaccia Amministrativa:** Ridimensionate e rese più compatte le card della schermata di gestione ricette per migliorare la leggibilità e la densità informativa.

* **Bonifica Modello `Recipe`:** Aggiornata la struttura SQLAlchemy per integrare il nuovo sistema immagini mantenendo piena compatibilità con il database esistente.

* **Risoluzione Conflitti Git:** Stabilizzata la struttura del repository durante l'integrazione della libreria immagini centralizzata e della nuova release v2.2.0.

---

### Note Tecniche

* Nuovo modello introdotto:

```python
MasterImage
```

* Nuovo collegamento relazionale:

```python
Recipe.image_id
```

* Compatibilità completa con database esistenti.

* Nessuna migrazione distruttiva richiesta.

---
