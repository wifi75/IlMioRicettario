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
