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
* **Pezzatura e Flotta Teglie:** L'utente può scegliere tra due metodi di calcolo. Nel metodo *Peso Impasto*, basta inserire i grammi desiderati; nel metodo *Teglie Assegnate*, il sistema carica le teglie consigliate per la ricetta permettendo all'utente di aggiungere le quantità tramite tasti visivi (+/-) puliti. Il calcolatore ridimensiona la lista della spesa automaticamente al grammo.
* **Esposizione della Forza (W):** Nella tabella degli ingredienti calcolati, la forza specifica delle singole farine utilizzate viene mostrata in modo distinto e pulito tramite un badge visivo. Gli elementi come acqua, olio o lievito lasceranno tale spazio completamente vuoto.
* **Selettore del Lievito:** Un menu a tendina permette di cambiare il tipo di lievito da "Fresco" a "Secco". Il sistema applicherà il coefficiente matematico memorizzato per ridurre o aumentare i grammi del lievito aggiornando i totali finali.
* **Cursore Idratazione:** Sbloccando l'interruttore dedicato, è possibile variare a piacere la percentuale di acqua della formula tramite uno slider scorrevole.
* **Schede dei Processi Dinamici:** In fondo alla pagina, l'interfaccia si divide in Tab. Se la ricetta prevede un Prefermento (Biga/Poolish) o la tecnica del Tangzhong (Roux), compariranno le schede dedicate con le dosi separate pronte da prelevare dal totale calcolato e le istruzioni operative per la loro preparazione.

---

## 🔐 3. Come Entrare nel Pannello Amministratore

Il Pannello Admin è l'area riservata per creare formule, gestire database ingredienti, anagrafica teglie e impostazioni del sito. 

1. Dal menù nella home page pubblica in basso clicca sul bottone **"Area Riservata Admin"** oppure digita nel browser: `http://IP_DEL_SERVER:8080/admin/login`
2. Inserisci le tue credenziali (Nome Utente e Password).
3. Una volta effettuato l'accesso, verrai reindirizzato direttamente alla **Gestione Formule ("Ricette")**, che costituisce il fulcro operativo del tuo ricettario (la vecchia rotta Dashboard è disattivata e reindirizza qui automaticamente per velocizzare il lavoro).
4. Per uscire in sicurezza in qualsiasi momento, clicca sul pulsante rosso **Logout** in fondo al menu laterale o sul tasto **Pannello Controllo Admin** posizionato nel footer qualora ti trovassi nella visualizzazione del sito pubblico.

---

## 🧫 4. Gestione dei Vari Pannelli Amministrativi

Una volta dentro l'area Admin, avrai a disposizione le sezioni principali nel menu di navigazione:

### A. Gestione Formule ("Ricette")
In questo pannello puoi creare i tuoi capolavori.
* **Editor Istruzioni (Quill.js):** Troverai integrato un editor avanzato stile Microsoft Word. Al salvataggio, il testo lineare viene memorizzato mantenendo i caratteri nativi di a capo (`\n`). Quando la ricetta viene renderizzata nel frontend, l'algoritmo autonomo di Jinja2 elabora il testo riga per riga, generando un elenco numerato progressivo e inserendo in grassetto la primissima parola di ogni riga.
* **Composizione Ingredienti & Valore W:** Quando inserisci una materia prima nel form, la cerchi e la selezioni dalla lista globale. Il sistema identificherà autonomamente se si tratta di farina o liquido e importerà il valore della sua forza (W) dal database madre (fissando tale valore tramite array nascosto per la precisione di archiviazione SQL).
* **Assegnazione Teglie:** Un pannello di interruttori ti permette di spuntare quali forme della tua flotta (rotonde, teglie in ferro blu, stampi da panettone) sono ottimali o idonee per l'impasto in lavorazione.

### B. L'Anagrafica Centralizzata ("Master Ingredienti")
Prima di aggiungere un ingrediente a una ricetta, esso deve esistere in questa lista globale. 
* Clicca su **Aggiungi Ingrediente**.
* Inserisci il nome (es. *Farina Manitoba*).
* **Controllo Interbloccato:** Il modulo di inserimento possiede un controllo JavaScript che impedisce a un ingrediente di essere contemporaneamente una farina e un liquido.
* **La Forza della Farina (W):** Se l'ingrediente che stai creando è marcato come "È una Farina", il sistema abiliterà il campo numerico del parametro $W$. Se non lo è (es. *Acqua*), l'indicatore verrà azzerato. Tale censimento renderà la creazione successiva delle ricette istantanea.

### C. L'Anagrafica Teglie ("Master Stampi")
Simile all'anagrafica ingredienti, questo dizionario globale permette di censire l'armamentario del panificatore. 
* Crea un nuovo stampo definendo un **Nome**, una **Tipologia Estetica** (Tonda, Rettangolare, ecc.) e, soprattutto, la **Capacità Numerica** in grammi (Es. `1200` per una teglia di focaccia 40x30). Il calcolatore in frontend moltiplicherà la capacità per il numero di teglie inserite dal panificatore.

### D. Impostazioni Globali: Lieviti e Design del Sito
In questa sezione gestisci la potenza del motore di calcolo e l'estetica del progetto.
* **Bilanciamento Lieviti:** Troverai due campi intuitivi (Grammi Fresco e Grammi Secco Equivalenti) per calcolare globalmente il rapporto di conversione e i parametri base di farina/liquidi usati nel Tangzhong (Roux).
* **Design e Temi Sito:** Questo pannello agisce sui *Settings* strutturali dell'interfaccia. Potrai scrivere il nome generale della panetteria, personalizzare il testo del sottotitolo nella Home Page e applicare con un clic il tuo **Tema Cromatico** preferito tra una lunga lista di stili (Es. *Antica Panetteria*, *Borgo Antico*, *Pizzeria Industriale*), mutando i colori dell'intero ecosistema.

### E. Sicurezza Account
Una sezione dedicata alla protezione del profilo amministratore. Ti permette di modificare la password di accesso inserendo la chiave attuale e definendo una nuova password (minimo 6 caratteri). Il sistema si occuperà di crittografarla tramite algoritmo sicuro (`password_hash`) in tempo reale, senza mai salvarla come testo in chiaro nel database locale SQLite.

---

## 💡 Consigli per un Bilanciamento Perfetto

Quando inserisci una nuova ricetta nel sistema come Amministratore, per fare in modo che la matematica del simulatore funzioni al 100% in modalità "Percentuale Baker", ricordati di:
1. Scegliere materie prime la cui anagrafica centrale sia correttamente "taggata" con l'opzione **Farina** attiva per la polvere principale e **Liquido** attiva per l'acqua/latte/birra.
2. Controllare a vista che nel tab del bilanciamento l'applicazione ti restituisca le icone relative, per permettere al cursore dell'idratazione di operare il giusto smistamento percentuale nel calcolatore finale in produzione.