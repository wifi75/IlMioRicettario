# CHANGELOG

## v2.1.0 - 2026-06-10

### Aggiunto
* **Rotta Wiki Front-End Sicura:** Creata la rotta pubblica `/wiki` all'interno di `routes/recipes.py` che genera ed espone il manuale tecnico dell'arte bianca. Il sistema è configurato per bypassare i blocchi di importazione legati alla classe di modello `wiki` minuscola.
* **Pulsante di Accesso alla Wiki:** Inserito un pulsante ad hoc, elegante e centrato, posizionato in cima a `recipes_list.html`, offrendo ai visitatori l'accesso diretto alla documentazione tecnica delle formule.
* **Template Espositivo `wiki_public.html`:** Sviluppato un nuovo template di visualizzazione pubblica posizionato nella root di `templates`, mantenendo lo stile grafico del ricettario.

### Modificato e Corretto
* **Sfondo Universale Alta Leggibilità:** Sostituito lo sfondo azzurrino sbiadito dei temi pubblici con la palette grigio ardesia chiaro `#f8fafc` del pannello di controllo admin. Massimizzato il contrasto di lettura globale.
* **Sanificazione Tema Forno di Paese:** Risolto definitivamente il problema del basso contrasto visivo; scuriti tutti i testi descrittivi e i titoli principali in blu notte e ardesia scuro. La lettera "W" e le diciture tecniche risultano ora nitide.
* **Centratura Assoluta dei Badge con Flexbox:** Riprogettati i CSS dei badge di forza ($W$) e dei tag condizionali (es. "TEST"). Grazie alle proprietà `inline-flex`, `align-items: center` e `justify-content: center`, i testi si auto-allineano al centro geometrico spaccato delle loro forme.
* **Risoluzione Crash Critici Python (`ImportError`):** Bonificato il file `routes/recipes.py` dagli errori di importazione ciclici legati alla classe del database, ripristinando la stabilità operativa dell'applicazione.

---

## v0.5.0 - 2026-06-08

### Aggiunto
* **Forza della Farina Sincronizzata (`w_value`):** Inserita la colonna `w_value` nel modello locale `RecipeIngredient` e configurata l'iniezione automatica a freddo nel database SQLite all'avvio.
* **Cattura Automatica Forza W:** Aggiornate le rotte `recipe_new` e `recipe_edit` in `routes/admin.py` per intercettare l'array `ing_w[]` dal form e blindare il valore W centralizzato all'interno della formula salvata.
* **Badge Visivo W sul Frontend Pubblico:** Introdotto un indicatore visivo scuro con testo giallo nella tabella del calcolatore pubblico per esporre la forza delle farine ai visitatori in modalità responsive.

### Modificato e Corretto
* **Isolamento Selettivo del W:** Corretta la logica visiva sia nel form amministrativo che nel frontend pubblico; il badge della forza (W) si attiva solo ed esclusivamente sulle farine, lasciando lo spazio vuoto e pulito per sale, zucchero, acqua e olio.
* **Restyling Interfaccia Calcolatore Teglie:** Eliminati i pulsanti doppioni nativi del browser e i testi fissi (+/-) nella sezione teglie pubblica. Ricreati pulsanti grafici Bootstrap con icone vettoriali grandi, puliti e con larghezza fissa anti-schiacciamento.
* **Unificazione Riga Totale Impasto:** Semplificata la riga di chiusura della tabella sul frontend in un'unica dicitura pulita "TOTAL IMPASTO" senza simboli grafici extra o frammentazioni.
* **Spostamento Tasto Pannello Admin:** Rimosso il pulsante nero "Pannello Controllo Admin" dalla cima della Home pubblica e integrato stabilmente nel footer del sito, posizionato sotto i crediti e il copyright.

---

## v0.4.0 - 2026-06-07

### Aggiunto
* **Anagrafica Centralizzata Ingredienti (`MasterIngredient`):** Introdotta la tabella dizionario nel database per standardizzare i componenti degli impasti.
* **Seeding Automatico del DB:** Configurato il pre-popolamento automatico all'avvio dell'applicazione con 13 ingredienti pilastro della panificazione se la tabella è vuota.
* **Interfaccia di Gestione Anagrafica:** Creata la schermata dedicata `/admin/ingredients/master` con form di inserimento rapido e tabella di riepilogo con eliminazione dei record dal DB.
* **Controllo JavaScript Interbloccato:** Script Vanilla JS lato client inserito nell'anagrafica per impedire la selezione simultanea dei flag "È una Farina" ed "È un Liquido".

### Modificato e Corretto
* **Risoluzione Crash "Pagina Bianca":** Disaccoppiate le query degli ingredienti master dal Context Processor globale (`@app.context_processor`) per eliminare ricorsioni e blocchi di sessione in SQLAlchemy. I dati ora vengono iniettati esplicitamente dalle rotte dei Blueprint interessati.
* **Robustezza delle Rotte Amministrative:** Inserito il controllo di sicurezza preventivo sulla sessione e sull'autenticazione dell'utente prima dell'estrazione dei dati.
* **Correzione Strutturale `base.html`:** Sistemati e bilanciati tutti i tag condizionali Jinja2 che frammentavano l'HTML, ripristinando la corretta chiusura dei contenitori della sidebar amministrativa e del blocco di login.

---

## v0.3.0 - 2026-06-05
* Rilascio iniziale, gestione autenticazione, database relazionale SQLite strutturato, moduli Biga/Poolish e Tangzhong client-side.