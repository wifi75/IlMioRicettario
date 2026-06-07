# CHATGPT CONTEXT

## PROGETTO
Il Mio Ricettario
Repository GitHub: https://github.com/wifi75/IlMioRicettario

---

## STACK TECNOLOGICO
* Python 3
* Flask (Flask-SQLAlchemy, Flask-Login)
* SQLite
* Bootstrap 5 & Bootstrap Icons
* HTML / CSS / JavaScript (Vanilla)
* Jinja2

---

## OBIETTIVO
Realizzare una piattaforma professionale per la gestione di ricette dinamiche. Il sistema non è un semplice ricettario statico: ogni ricetta può attivare moduli e motori di calcolo configurabili dal backend e ricalcolati in tempo reale nel frontend.

---

## ARCHITETTURA & MODULI PREVISTI

Ogni ricetta può abilitare o disabilitare funzionalità specifiche (Features) tramite interruttori nel pannello admin.

### 1. Modulo Panetti / Pezzature
Permette di configurare:
* Numero pezzi / panetti
* Peso singolo pezzo

### 2. Modulo Teglie / Stampi
Permette di calcolare l'impasto in base alla superficie:
* Numero teglie / stampi
* Formato e dimensioni teglia (es. rettangolare, tonda)

### 3. Modulo Lievito & Conversioni
Gestisce la scelta del tipo di agente lievitante:
* Lievito di Birra Fresco
* Lievito di Birra Secco (es. Caputo)
* Lievito Madre (futuro)
*La proporzione di conversione tra fresco e secco è configurabile globalmente nelle impostazioni di sistema.*

### 4. Modulo Tangzhong (Water Roux)
Configurabile globalmente da backend:
* Percentuale di farina da isolare (Standard: 5%)
* Moltiplicatore del liquido (Standard: 5×)
*Logica:* Quando attivato su una ricetta, il sistema calcola la porzione di Tangzhong, la mostra in una sezione dedicata e sottrae automaticamente i quantitativi di farina e liquido dalla ricetta principale.

### 5. Moduli Avanzati (Roadmap)
* Pre-impasti: Poolish e Biga gestione automatica delle percentuali di idratazione.

---

## SEZIONE WIKI
Sezione enciclopedica integrata per istruire l'utente su concetti di panificazione:
* Argomenti: Lievito fresco/secco, Tangzhong, Poolish, Biga, Idratazione, Autolisi.
* Gestione dei contenuti (CRUD) completamente centralizzata nel backend amministrativo.

---

## STRUTTURA DATABASE (MODELLI SQLALCHEMY)
* `User`: Gestione utenti e credenziali amministrative (`is_admin`).
* `MasterIngredient`: Anagrafica centralizzata degli ingredienti (ID, nome, flag `is_flour`, flag `is_liquid`).
* `Recipe`: Testata della ricetta (titolo, descrizione, idratazione target, ecc.).
* `RecipeIngredient`: Collegamento tra ricetta e ingredienti (peso, ordine, legame opzionale con MasterIngredient).
* `RecipeFeature`: Flag booleani per attivare/disattivare i singoli moduli su ogni ricetta.
* `RecipeParameter`: Valori e configurazioni specifiche salvate per i moduli attivi della ricetta.
* `Setting`: Configurazione globale dei parametri di calcolo (es. ratio lieviti, percentuali tangzhong, nome sito).
* `WikiArticle`: Gestione articoli della Wiki.

---

## REGOLE DI SVILUPPO (TASSATIVE)
1. **File Completi:** Fornire sempre codici interi pronti al copia-incolla. No patch parziali, no commenti placeholder del tipo `# ... resto del codice immutato ...`.
2. **Integrità:** Non rompere le funzionalità esistenti o le relazioni tra i modelli.
3. **Indicazione File:** Specificare sempre con chiarezza il percorso del file da modificare.
4. **Isolamento delle Query:** Non appesantire il Context Processor globale (`@app.context_processor`) con query pesanti o dinamiche che possono generare ricorsioni (loop) o blocchi di sessione del database. Passare i dati specifici tramite i render dei Blueprint interessati.
5. **Mobile-First & UI:** Sfruttare al massimo le utility responsive di Bootstrap 5. Layout pulito, moderno (interfaccia scura per la sidebar admin, card bianche minimaliste su sfondo slate leggero per i contenuti).

---

## STATO ATTUALE DEL PROGETTO (COMPLETATO)
* **Sicurezza & Login:** Autenticazione amministratore funzionante tramite Flask-Login. Account di default (`admin`/`admin123`) generato automaticamente all'avvio.
* **Layout Base Consolidato:** File `base.html` corretto e privo di bug condizionali. Gestisce correttamente la sidebar per gli utenti loggati e isola il form di login per gli anonimi senza rompere i tag del DOM.
* **Anagrafica Centralizzata Ingredienti:** Creata la tabella `MasterIngredient`. Il file `app.py` effettua il seeding automatico (pre-popolamento) con 13 ingredienti base della panificazione se la tabella risulta vuota.
* **Pannello Gestione Anagrafica:** Schermata `/admin/ingredients/master` completata con form di inserimento (con controllo JavaScript interbloccato per impedire che un ingrediente sia contemporaneamente farina e liquido) e tabella di riepilogo con eliminazione.
* **Calcolatore Core:** Calcolo automatico delle farine totali, dei liquidi totali e della percentuale reale di idratazione dell'impasto nel backend amministrativo.

---

## ROADMAP PROSSIMI PASSI (V1)
* **Integrazione Form Ricette:** Modificare i form di creazione e modifica ricetta (`recipe_form.html` e `recipe_edit_form.html`) in modo che il campo di inserimento degli ingredienti utilizzi una tendina (select o datalist) basata sulla lista `master_ingredients_list` passata dalle rotte, ereditando automaticamente le proprietà tecniche del database.
* **Attivazione Interruttori Feature:** Collegare gli switch delle feature nella modifica della ricetta per salvare le preferenze nel DB.
* **Sviluppo Frontend Pubblico:** Creazione dei motori JavaScript per il ricalcolo dinamico delle pezzature e dei lieviti sul lato client durante la visualizzazione pubblica della ricetta.