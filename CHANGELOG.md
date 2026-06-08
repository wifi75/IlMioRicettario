# CHANGELOG

## v0.5.0 - 2026-06-08

### Aggiunto
* **Forza della Farina Sincronizzata (`w_value`):** Inserita la colonna `w_value` nel modello locale `RecipeIngredient` e configurata l'iniezione automatica a freddo nel database SQLite all'avvio.
* **Cattura Automatica Forza W:** Aggiornate le rotte `recipe_new` e `recipe_edit` in `routes/admin.py` per intercettare l'array `ing_w[]` dal form e blindare il valore W centralizzato all'interno della formula salvata.
* **Badge Visivo W sul Frontend Pubblico:** Introdotto un indicatore visivo scuro con testo giallo nella tabella del calcolatore pubblico per esporre la forza delle farine ai visitatori in modalità responsive.

### Modificato e Corretto
* **Isolamento Selettivo del W:** Corretta la logica visiva sia nel form amministrativo che nel frontend pubblico; il badge della forza (W) si attiva solo ed esclusivamente sulle farine, lasciando lo spazio vuoto e pulito per sale, zucchero, acqua e olio (eliminati i trattini "—" superflui).
* **Restyling Interfaccia Calcolatore Teglie:** Eliminati i pulsanti doppioni nativi del browser e i testi fissi (+/-) nella sezione teglie pubblica. Ricreati pulsanti grafici Bootstrap con icone vettoriali grandi, puliti e con larghezza fissa anti-schiacciamento.
* **Unificazione Riga Totale Impasto:** Semplificata la riga di chiusura della tabella sul frontend in un'unica dicitura pulita "TOTAL IMPASTO" senza simboli grafici extra o frammentazioni.
* **Spostamento Tasto Pannello Admin:** Rimosso il pulsante nero "Pannello Controllo Admin" dalla cima della Home pubblica (che spezzava il layout) e integrato stabilmente nel footer del sito, posizionato sotto i crediti e il copyright.

---

## v0.4.0 - 2026-06-07

### Aggiunto
* **Anagrafica Centralizzata Ingredienti (`MasterIngredient`):** Introdotta la tabella dizionario nel database per standardizzare i componenti degli impasti.
* **Seeding Automatico del DB:** Configurato il pre-popolamento automatico all'avvio dell'applicazione con 13 ingredienti pilastro della panificazione (Farine, Liquidi, Lieviti, Grassi, Zuccheri) se la tabella è vuota.
* **Interfaccia di Gestione Anagrafica:** Creata la schermata dedicata `/admin/ingredients/master` con form di inserimento rapido e tabella di riepilogo con eliminazione dei record dal DB.
* **Controllo JavaScript Interbloccato:** Script Vanilla JS lato client inserito nell'anagrafica per impedire la selezione simultanea dei flag "È una Farina" ed "È un Liquido".

### Modificato e Corretto
* **Risoluzione Crash "Pagina Bianca":** Disaccoppiate le query degli ingredienti master dal Context Processor globale (`@app.context_processor`) per eliminare ricorsioni e blocchi di sessione in SQLAlchemy. I dati ora vengono iniettati esplicitamente dalle rotte dei Blueprint interessati.
* **Robustezza delle Rotte Amministrative:** Inserito il controllo di sicurezza preventivo sulla sessione e sull'autenticazione dell'utente (`current_user.is_authenticated`) prima dell'estrazione dei dati.
* **Correzione Strutturale `base.html`:** Sistemati e bilanciati tutti i tag condizionali Jinja2 (`{% if %}` / `{% else %}`) che frammentavano l'HTML, ripristinando la corretta chiusura dei contenitori della sidebar amministrativa e del blocco di login.

---

## v0.3.0 - 2026-06-05

### Aggiunto
* Sistema autenticazione amministratore
* Dashboard amministrazione
* Gestione ricette (Creazione, Eliminazione, Visualizzazione dettaglio)
* Gestione ingredienti ricetta ed eliminazione rapida
* Motore di calcolo core in backend: Farine totali, Liquidi totali, Percentuale di Idratazione reale
* Supporto ingredienti classificabili come Tipo Farina e Tipo Liquido
* Modelli di database strutturali: `RecipeFeature`, `RecipeParameter`, `Setting`
* Interfaccia responsive Mobile-First basata su Bootstrap 5 e Bootstrap Icons
* Database relazionale SQLite tramite Flask-SQLAlchemy

### Migliorato
* Layout generale del pannello di amministrazione
* Visualizzazione delle statistiche e dei riepiloghi tecnici della ricetta
* Interfaccia grafica della dashboard principale
* Adattabilità e compatibility del layout su smartphone e tablet

---

## Roadmap Prossimi Passi (Verso la V1)
* **Aggancio Form-Anagrafica:** Integrazione della lista ingredienti master nei form delle ricette per l'autocompletamento in digitazione.
* **Parametri Dinamici:** Abilitazione e salvataggio dei moduli (Panetti, Teglie, Tangzhong) per singola ricetta nel database.
* **Percentuali Panificatore:** Calcolo automatico in backend dei pesi percentuali basati sulla farina al 100%.
* **Motori Frontend JS:** Sviluppo degli slider per idratazione variabile e ricalcolo in tempo reale delle dosi per panetti/teglie sul client.