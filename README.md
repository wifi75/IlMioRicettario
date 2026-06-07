# 🧫 Il Mio Ricettario Panificazione - Professional Suite

![Versione](https://img.shields.io/badge/version-v0.6.0-orange?style=for-the-badge)
![Flask](https://img.shields.io/badge/Framework-Flask--Python-blue?style=for-the-badge&logo=flask)
![Database](https://img.shields.io/badge/Database-SQLite%20%2B%20SQLAlchemy-green?style=for-the-badge&logo=sqlite)

> Un'applicazione web avanzata e scientifica dedicata all'arte bianca e alla pasticceria professionale. Gestisci il tuo ricettario, calcola i bilanciamenti degli impasti, monitora la forza delle farine ($W$) e converti i lieviti con precisione sartoriale.

---

## 🚀 Novità dell'Ultima Release (v0.6.0)

Abbiamo trasformato il ricettario in uno strumento tecnico per panificatori esigenti:
* 🔒 **Migrazioni Database Sicure:** Integrazione di `Flask-Migrate` (Alembic) per aggiornare la struttura delle tabelle senza mai più perdere o cancellare le ricette salvate.
* 🌾 **Gestione della Forza ($W$):** Nuova colonna nell'Anagrafica Centralizzata. Un'interfaccia intelligente mostra il campo della forza solo quando si seleziona un ingrediente di tipo farina.
* 🧪 **Calcolatore Proporzionale dei Lieviti:** Ribaltata la logica commerciale rigida del coefficiente 3.0. Ora inserisci tu il rapporto reale basandoti sulle marche professionali (es. *Caputo Secco*) e il sistema sincronizzerà tutti i calcolatori del sito all'istante.

---

## ✨ Funzionalità Chiave

### 🖥️ Pannello Amministratore (Centralizzato)
* **Anagrafica Materie Prime:** Gestione globale degli ingredienti con classificazione dinamica (Farine con valore $W$, Liquidi per l'idratazione, Altro).
* **Configuratore Scientifico:** Inserisci la corrispondenza empirica tra grammi di lievito fresco e secco (es. `3g` fresco $\rightarrow$ `1.5g` secco) per generare automaticamente il coefficiente matematico globale di conversione.
* **CRUD Ricette Completo:** Crea, modifica e cancella le preparazioni, definendo l'ordine esatto degli ingredienti e i passaggi operativi.

### 🍕 Lato Utente / Simulatore (In Sviluppo)
* Visualizzazione pulita delle ricette tramite URL statici ottimizzati (`/recipe/<slug>`).
* Motore JavaScript per il ricalcolo istantaneo delle proporzioni e la conversione dinamica dei lieviti a schermo.

---

## 🛠️ Stack Tecnologico

L'applicazione è strutturata seguendo le migliori pratiche dello sviluppo web in Python:

📦 IlMioRicettario
┣ 📂 models           # Modelli del Database (User, Recipe, Ingredient, Setting)
┣ 📂 routes           # Controller e Rotte divise per Blueprint (Admin, Public)
┣ 📂 templates        # File HTML dinamici con motore Jinja2
┣ 📂 static           # Asset grafici, CSS (Bootstrap 5) e script JS personali
┣ 📂 migrations       # Storico dei cambiamenti strutturali del database SQL
┣ 📜 app.py           # Entry point dell'applicazione e configurazioni
┗ 📜 extensions.py    # Inizializzazioni condivise (SQLAlchemy, LoginManager, Migrate)

---

## 💾 Installazione e Avvio Locale

Segui questi passaggi per avviare il progetto sul tuo computer:

1. **Clona la repository:**
   ```bash
   git clone [https://github.com/tuo-username/IlMioRicettario.git](https://github.com/tuo-username/IlMioRicettario.git)
   cd IlMioRicettario