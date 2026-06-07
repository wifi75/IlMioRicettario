# 🧫 Il Mio Ricettario Panificazione - Professional Suite

![Versione](https://img.shields.io/badge/version-v0.7.0-orange?style=for-the-badge)
![Framework](https://img.shields.io/badge/Framework-Flask--Python-blue?style=for-the-badge&logo=flask)
![Database](https://img.shields.io/badge/Database-SQLite%20%2B%20SQLAlchemy-green?style=for-the-badge&logo=sqlite)
![Linux Deploy](https://img.shields.io/badge/Server-Linux%20%2B%20Gunicorn-red?style=for-the-badge&logo=linux)

> Benvenuto nel tuo Ricettario di Panificazione Scientifico. Questa applicazione web ti permette di gestire un database centralizzato di ingredienti, monitorare la forza delle farine (W), calcolare la conversione dei lieviti in tempo reale e gestire tecniche avanzate come il pre-impasto o il Tangzhong. 

Questa guida ti spiegherà passo-passo come installare lo script su un server Linux, come accedervi da remoto dal tuo computer o smartphone e come gestire il pannello di controllo Amministratore.

---

## 🚀 Funzionalità Principali della v0.7.0

* 🔒 **Sicurezza del Database:** Gestione tramite Flask-Migrate. La struttura si aggiorna senza mai rischiare di cancellare o perdere le ricette già salvate.
* 🌾 **Anagrafica Farine (W):** Mappatura della forza delle farine con campi intelligenti che compaiono solo quando necessario.
* 🧪 **Rapporto Lieviti Personalizzato:** Puoi decidere tu a quanti grammi di lievito secco corrisponde il lievito fresco, adattando il calcolatore alle marche professionali (es. Caputo).
* 🥣 **Motore Tangzhong Dinamico:** Se attivo, il sistema calcola i pesi esatti di farina e liquido da sottrarre alla ricetta base e mostra all'utente la procedura passo-passo per la cottura in padella del Roux.

---

## 💾 Guida all'Installazione su Server Linux

Per fare in modo che il sito sia sempre attivo e raggiungibile da internet, va installato su un server Linux (es. Ubuntu Server) utilizzando Gunicorn (l'application server) e Systemd (il gestore di servizi di Linux).

### Step 1: Preparazione del Server Linux
Connettiti al tuo server tramite terminale SSH e installa i componenti base richiesti dal sistema:
sudo apt update
sudo apt install python3-pip python3-venv git -y

### Step 2: Scaricamento e Configurazione del Codice
Spostati nella cartella web del server, scarica lo script da GitHub e configura l'ambiente protetto (ambiente virtuale Python):
cd /var/www
sudo git clone https://github.com/wifi75/IlMioRicettario.git
sudo chown -R $USER:$USER /var/www/IlMioRicettario
cd IlMioRicettario

python3 -m venv venv
source venv/bin/activate
pip install flask flask_sqlalchemy flask_login flask_migrate werkzeug gunicorn
flask db upgrade
deactivate

### Step 3: Configurazione del Servizio Automatico (Systemd)
Creiamo un servizio di sistema per fare in modo che Linux mantenga il sito attivo in background e lo riavvii da solo se il server si spegne o si riavvia.

Apri l'editor di testo del server:
sudo nano /etc/systemd/system/ricettario.service

Incolla dentro il file questo blocco di testo (ricordati di cambiare "tuo_utente" con il vero nome del tuo utente sul server Linux):
[Unit]
Description=Istanza Gunicorn per Il Mio Ricettario
After=network.target

[Service]
User=tuo_utente
Group=www-data
WorkingDirectory=/var/www/IlMioRicettario
ExecStart=/var/www/IlMioRicettario/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:8080 app:app
Restart=always

[Install]
WantedBy=multi-user.target

(Per salvare e uscire da nano premi CTRL+X, poi premi Y e infine premi Invio)

### Step 4: Avvio del Sito su Linux
Attiva il servizio appena creato e digitalo come prioritario all'avvio del server:
sudo systemctl daemon-reload
sudo systemctl enable ricettario
sudo systemctl start ricettario

---

## 🖥️ Come Raggiungere il Sito dal Browser

Una volta avviato il servizio su Linux, l'applicazione è attiva e in ascolto sulla porta 8080. Per navigare sul sito dal tuo computer, tablet o smartphone connesso a internet, apri il browser (Chrome, Safari, Edge) e digita nella barra degli indirizzi:

http://IP_DEL_TUO_SERVER:8080

(Sostituisci "IP_DEL_TUO_SERVER" con l'indirizzo IP numerico del tuo server Linux, ad esempio http://192.168.1.50:8080 oppure l'IP pubblico del tuo VPS cloud).

---

## 🔐 Guida Completa di Amministrazione (Pannello Admin)

Il sito si divide in due parti: la parte pubblica (il catalogo delle formule accessibile a tutti) e la zona di amministrazione (dove puoi aggiungere ingredienti, modificare coefficienti e creare ricette).

### 1. Come Entrare nel Pannello di Controllo
Per accedere alla schermata di Login amministrativa, aggiungi `/admin/login` alla fine del tuo indirizzo web, in questo modo:

http://IP_DEL_TUO_SERVER:8080/admin/login

Ti troverai davanti a una schermata sicura che ti chiederà Nome Utente e Password.

### 2. Credenziali di Fabbrica (Primo Accesso)
Al primo avvio, lo script genera automaticamente nel database un utente amministratore standard con le seguenti credenziali:
* **Nome Utente:** admin
* **Password Temporanea:** admin123

Digita questi dati per effettuare l'accesso ed entrare nella Dashboard principale.

### 3. Come Modificare la Password di Amministrazione
Per motivi di sicurezza, la password sul database non viene mai salvata in chiaro (come testo semplice), ma viene crittografata tramite un algoritmo sicuro chiamato "password_hash". Per cambiare la password di amministrazione ed impostarne una tua personale, segui questa procedura guidata:

Entra nel server Linux tramite terminale, spostati nella cartella del progetto ed avvia la console interattiva di Python:
cd /var/www/IlMioRicettario
source venv/bin/activate
python

Ti comparirà il terminale di Python (riconoscibile dai simboli >>>). Incolla queste righe di codice una alla volta premendo Invio:
from app import app
from extensions import db
from models.user import User
from werkzeug.security import generate_password_hash

ctx = app.app_context()
ctx.push()

user = User.query.filter_by(username='admin').first()
user.password_hash = generate_password_hash('SCRIVI_QUI_LA_TUA_NUOVA_PASSWORD')
db.session.commit()
exit()

(Sostituisci 'SCRIVI_QUI_LA_TUA_NUOVA_PASSWORD' con la parola d'ordine segreta che preferisci, mantenendo le virgolette singole. Una volta digitato exit() la nuova password è attiva all'istante e puoi usarla per entrare nel sito).

Disattiva infine l'ambiente virtuale sul server:
deactivate

---

## 📊 Comandi Utili per la Gestione del Server

Se effettui modifiche ai file del codice o ai template HTML e vuoi vederle applicate sul sito internet, devi dire a Linux di riavviare l'applicazione in background. Usa questi comandi rapidi:

* **Controllare se il sito sta girando bene:** `sudo systemctl status ricettario`
* **Applicare modifiche e riavviare il sito:** `sudo systemctl restart ricettario`
* **Vedere la lista degli errori in tempo reale:** `sudo journalctl -u ricettario -f`

---

## 📈 Sviluppi Futuri della Roadmap

- [ ] Idratazione Automatica: Calcolo in tempo reale della percentuale di liquidi totali sulla farina direttamente nella scheda di inserimento.
- [ ] Media Ponderata del W: Calcolo automatico della forza finale del mix di farine quando se ne usano diverse nella stessa ricetta.

---

⭐️ Progetto ideato, architettato e sviluppato con passione da **Tiziano Cassone**.