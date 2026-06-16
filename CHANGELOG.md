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
