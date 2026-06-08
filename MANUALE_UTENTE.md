# 📖 Manuale Utente - Guida all'Utilizzo del Ricettario Scientifico

Benvenuto nel manuale d'uso ufficiale dell'applicazione. Questa guida è stata scritta per spiegare in modo semplice e immediato come raggiungere il servizio, come navigare tra le ricette pubbliche e come sfruttare al massimo il pannello di controllo Amministratore per il bilanciamento professionale degli impasti.

---

## 🌐 1. Come Raggiungere l'Applicazione (Indirizzo e Porta)

L'applicazione gira come un servizio web continuo. Per aprirla sul tuo computer, tablet o smartphone, assicurati di essere connesso alla rete e digita l'indirizzo nella barra del tuo browser internet (Chrome, Safari, Edge, Firefox):

* **Se usi l'app sul tuo computer in locale (Sviluppo):** http://127.0.0.1:8080
* **Se usi l'app installata sul Server Linux (Produzione):** http://IP_DEL_SERVER:8080
  *(Nota: La porta di ascolto predefinita configurata per il servizio è la **8080**)*

---

## 🍕 2. L'Interfaccia Pubblica (Il Simulatore Dinamico)

La pagina principale dell'applicazione mostra il catalogo di tutte le ricette approvate e pubblicate. Cliccando su una ricetta (ad esempio *"Panini all'olio"*), entrerai nel **Simulatore ad Alta Precisione**.

Questa schermata permette a qualsiasi utente di personalizzare l'impasto prima di iniziare a impastare:
* **Pezzatura su Misura:** Inserendo il Numero di Panetti desiderati e il Peso di ogni singolo panetto, il motore dell'app ricalcolerà istantaneamente i grammi di ogni singolo ingrediente per darti il peso finale esatto, azzerando gli sprechi.
* **Selettore del Lievito:** Un menu a tendina permette di cambiare il tipo di lievito da "Fresco" a "Secco". Il sistema applicherà il coefficiente matematico memorizzato per ridurre i grammi del secco e riordinare le proporzioni degli altri ingredienti.
* **Cursore Idratazione:** Spostando la barra dell'idratazione (es. dal 52% al 70%), il sistema modificherà la quantità di acqua o latte per ammorbidire l'impasto secondo le tue esigenze tecnologiche.
* **Schede dei Processi Dinamici:** In fondo alla pagina, l'interfaccia si divide in Tab. Se la ricetta prevede un Prefermento (Biga/Poolish) o la tecnica del Tangzhong (Roux), compariranno le schede dedicate con le dosi separate da prelevare dal totale e le istruzioni di cottura passo-passo.

---

## 🔐 3. Come Entrare nel Pannello Amministratore

Il Pannello Admin è l'area riservata in cui puoi creare nuove ricette, gestire gli ingredienti e modificare i parametri del sito. 

1. Per raggiungere la schermata di login, digita nel browser: `http://IP_DEL_SERVER:8080/admin/login`
2. Inserisci le tue credenziali (Nome Utente e Password).
3. Una volta effettuato l'accesso, verrai reindirizzato direttamente alla **Gestione Formule ("Ricette")**, che costituisce il fulcro operativo del tuo ricettario (la vecchia rotta Dashboard è disattivata e reindirizza qui automaticamente per velocizzare il lavoro).
4. Per uscire in sicurezza in qualsiasi momento, clicca sul pulsante **Logout** nel menu.

---

## 🧫 4. Gestione dei Vari Pannelli Amministrativi

Una volta dentro l'area Admin, avrai a disposizione le sezioni principali nel menu di navigazione:

### A. Gestione Formule ("Ricette")
In questo pannello puoi creare i tuoi capolavori.
* **Nuova Ricetta & Modifica:** Troverai integrato un editor avanzato stile Microsoft Word (Quill.js). Questo strumento WYSIWYG ti permette di formattare il testo, gestire i font e gli elenchi direttamente dal browser. Al salvataggio, il testo lineare viene memorizzato mantenendo i caratteri nativi di a capo (`\n`).
* **Algoritmo di Impaginazione Autonomo:** Quando la ricetta viene renderizzata nel frontend pubblico o nel dettaglio admin, il sistema elabora il testo riga per riga. Genera automaticamente un elenco numerato progressivo ordinato (1., 2., 3...) e inserisce in grassetto (`<strong>`) in automatico la primissima parola di ogni riga (es. "Impasta a velocità..." diventa "<strong>Impasta</strong> a velocità...").
* **Composizione Ingredienti:** Entrando nel dettaglio di una ricetta, puoi inserire le materie prime cercandole tramite una comoda tendina dall'anagrafica centralizzata e impostando il loro peso base.
* **Feature Toggles (Interruttori Tecnici):** In fondo alla pagina di modifica della ricetta, puoi attivare o disattivare le funzioni speciali per quella specifica formula:
  * *Abilita Input N. Pezzi / Peso Panetto* (per attivare il calcolo geometrico nel frontend).
  * *Abilita Menu Tipo Lievito* (per permettere la conversione fresco/secco).
  * *Abilita Opzione Tangzhong* (per attivare il calcolo e il tab del Water Roux).

### B. L'Anagrafica Centralizzata ("Master Ingredienti")
Prima di aggiungere un ingrediente a una ricetta, esso deve esistere in questa lista globale. Serve a dare un'identità scientifica alle materie prime.
* Clicca su **Aggiungi Ingrediente**.
* Inserisci il nome (es. *Farina Tipo 00*, *Acqua*, *Sale Marino*).
* **Controllo Interbloccato:** Il modulo di inserimento possiede un controllo JavaScript che impedisce a un ingrediente di essere contemporaneamente una farina e un liquido.
* **I Toggle Tipologia:** Spunta se l'ingrediente è un *Liquido* (fondamentale per il calcolo dell'idratazione) o se è una *Farina*.
* **Il Valore W (Forza della Farina):** Se spunti il toggle "Farina", apparirà un campo numerico dedicato. Inserisci la forza della farina (es. `320`). Se l'ingrediente non è una farina, il sistema nasconderà il campo e lo imposterà a 0 automaticamente.

### C. Il Pannello "Impostazioni Lieviti & Parametri Globali"
In questa sezione gestisci la potenza del motore di calcolo del sito.
* Troverai un modulo con due campi intuitivi: **Grammi Fresco** e **Grammi Secco Equivalenti** per la conversione automatica delle ricette.
* **Parametri Tangzhong:** Gestione centralizzata dei coefficienti per il Water Roux (Standard: 5% di farina da isolare e moltiplicatore idrico 5×).

### D. Sicurezza Account
Una sezione dedicata alla protezione del profilo amministratore. Ti permette di modificare la password di accesso inserendo la chiave attuale e definendo una nuova password (minimo 6 caratteri). Il sistema si occuperà di crittografarla tramite algoritmo sicuro (`password_hash`) in tempo reale, senza mai salvarla come testo in chiaro nel database.

---

## 💡 Consigli per un Bilanciamento Perfetto

Quando inserisci una nuova ricetta nel sistema come Amministratore, per fare in modo che la matematica del simulatore funzioni al 100% in modalità "Percentuale Baker", ricordati di:
1. Spuntare sempre la casella **"Farina"** sull'ingrediente principale (o sulle farine miscelate), in modo che il sistema sappia qual è il parametro che comanda il 100% della formula.
2. Spuntare sempre la casella **"Liquido"** sull'acqua, sul latte o sulla birra, per permettere al cursore dell'idratazione di fare i ricalcoli in tempo reale.