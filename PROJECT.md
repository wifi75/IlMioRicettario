# CHATGPT CONTEXT (V1 - Milestone v0.3.0)

## PROGETTO
* **Nome:** Il Mio Ricettario
* **Versione:** V1 (In sviluppo attivo)
* **Milestone Corrente:** v0.3.0 - Base backend e anagrafica DB completate.
* **Repository GitHub:** https://github.com/wifi75/IlMioRicettario

---

## DESCRIZIONE & OBIETTIVI
Il Mio Ricettario è una piattaforma web professionale per la gestione di ricette dinamiche, focalizzata sul mondo dei lievitati (Pane, Pizza, Focacce, Panini, Grandi Lievitati). A differenza di un ricettario statico, ogni ricetta può attivare moduli e motori di calcolo configurabili dal backend che espongono interfacce interattive di ricalcolo in tempo reale nel frontend.

---

## STACK TECNOLOGICO
* **Backend:** Python 3 + Flask (Flask-SQLAlchemy, Flask-Login)
* **Database:** SQLite
* **Frontend:** Bootstrap 5, Bootstrap Icons, HTML5, CSS3, JavaScript (Vanilla)
* **Motore di Template:** Jinja2

---

## ARCHITETTURA DEI MODULI (FEATURES)
Ogni ricetta può abilitare o disabilitare funzionalità specifiche (Features) tramite interruttori nel pannello admin, salvati nel modello `RecipeFeature`:

1. **Modulo Panetti / Pezzature:** Configurazione di Numero Pezzi e Peso Singolo Pezzo.
2. **Modulo Teglie / Stampi:** Calcolo della quantità di impasto necessaria basata sulla superficie di teglie rettangolari o tonde.
3. **Modulo Lievito & Conversioni:** Scelta dell'agente lievitante (Fresco, Secco Caputo, o Madre). La proporzione di conversione (Ratio) è definita globalmente nelle impostazioni.
4. **Modulo Tangzhong (Water Roux):** Sottrae automaticamente il 5% della farina totale e un moltiplicatore 5× di liquido dall'impasto principale per isolarli in una sezione dedicata (i coefficienti sono modificabili globalmente).
5. **Moduli Avanzati (Pre-impasti):** Gestione e calcolo automatizzato di Poolish e Biga.

---

## STRUTTURA DATABASE (MODELLI SQLALCHEMY)
* `User`: Amministratori e credenziali di accesso.
* `MasterIngredient`: Dizionario centralizzato degli ingredienti (ID, nome, flag `is_flour`, flag `is_liquid`).
* `Recipe`: Testata della ricetta (titolo, istruzioni, idratazione target, tempi di autolisi, puntata, appretto).
* `RecipeIngredient`: Ingredienti associati alla singola ricetta (quantità, unità, ordine, flag tecnici).
* `RecipeFeature`: Flag booleani per abilitare/disabilitare i singoli motori di calcolo sulla ricetta.
* `RecipeParameter`: Parametri di configurazione locali della ricetta (es. peso panetto impostato).
* `Setting`: Configurazione globale dei parametri del sito (rapporto lieviti, parametri tangzhong, unità di misura).
* `WikiArticle`: Articoli enciclopedici della sezione Wiki (CRUD completo).

---

## REGOLE DI SVILUPPO (TASSATIVE)
1. **File Completi:** Fornire sempre codici interi pronti al copia-incolla per evitare frammentazioni o omissioni.
2. **Nessun Loop nel Database:** Non appesantire il Context Processor globale (`@app.context_processor`) con query dinamiche o pesanti che possono generare ricorsioni (loop) o blocchi di sessione. Passare i dati specifici (come la lista ingredienti master) esplicitamente tramite le rotte dei Blueprint interessati.
3. **Isolamento Condizionale:** Mantenere i tag condizionali di Jinja (`{% if %}`) strutturalmente solidi e bilanciati per non interrompere il rendering dell'HTML (`base.html`).
4. **Mobile First:** Garantire la totale responsività della UI su Smartphone, Tablet e Desktop sfruttando le classi native di Bootstrap 5.

---

## STATO ATTUALE (COMPLETATO & COLOGATO SU GIT)
* **Autenticazione:** Sistema di Login/Logout amministrativo funzionante. Account di default (`admin`/`admin123`) generato in automatico nel database se assente.
* **Layout Base Consolidato:** File `base.html` corretto e privo di bug strutturali. Gestisce la sidebar scura a sinistra per l'admin e isola la visualizzazione anonima.
* **Anagrafica Centralizzata Ingredienti:** Creata la tabella `MasterIngredient`. Il file `app.py` effettua il seeding automatico (pre-popolamento) con 13 ingredienti base della panificazione se la tabella è vuota.
* **Pannello Amministrativo Ingredienti:** Schermata `/admin/ingredients/master` completata e funzionante al 100%, comprensiva di form di inserimento (con controllo JS interbloccato farina/liquido) e tabella con eliminazione dei record.
* **Core Calcoli:** Calcolo dinamico in backend di farine totali, liquidi totali e percentuale reale di idratazione.
* **Git & Backup:** Codice sorgente e repository locale e remoto (`origin/main`) totalmente sincronizzati e puliti (*working tree clean*).