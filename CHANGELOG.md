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
