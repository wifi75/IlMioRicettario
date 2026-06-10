Markdown
# 🧫 Il Mio Ricettario Panificazione - Professional Suite

![Versione](https://img.shields.io/badge/version-v2.1.0-orange?style=for-the-badge)
![Framework](https://img.shields.io/badge/Framework-Flask--Python-blue?style=for-the-badge&logo=flask)
![Database](https://img.shields.io/badge/Database-SQLite%20%2B%20SQLAlchemy-green?style=for-the-badge&logo=sqlite)
![Linux Deploy](https://img.shields.io/badge/Server-Linux%20%2B%20Gunicorn-red?style=for-the-badge&logo=linux)

> Benvenuto nel tuo Ricettario di Panificazione Scientifico. Questa applicazione web ti permette di gestire un database centralizzato di ingredienti, monitorare la forza delle farine (W), calcolare la conversione dei lieviti in tempo reale, monitorare l'idratazione in tempo reale e gestire techniques avanzate come la prefermentazione complessa (Biga/Poolish) o il Tangzhong.

Questa guida ti spiegherà passo-passo come installare lo script su un server Linux, come accedervi da remoto dal tuo computer o smartphone e come gestire il pannello di controllo Amministratore.

---

## 🚀 Funzionalità Principali della v2.1.0

* 📝 **Editor Avanzato Stile Microsoft Word:** Form di creazione e modifica ricette aggiornati con l'integrazione di Quill.js (WYSIWYG) per gestire font, allineamenti e modifiche estetiche direttamente dal browser.
* 🧠 **Algoritmo di Impaginazione Intelligente:** Il sistema elabora le istruzioni salvate in modo semplice, genera automaticamente elenchi numerati progressivi e applica il grassetto (`<strong>`) in modo automatico alla primissima parola di ogni riga.
* 🧪 **Calcolatore Core & Simulatore Analitico:** Ricalcolo client-side istantaneo dei quantitativi idrici, delle percentuali Baker e riscalatura automatica dell'impasto in base al peso target o alla pezzatura (numero panetti).
* 🥣 **Motore Tangzhong Dinamico:** Se attivo, il sistema isola automaticamente la farina (5%) e applica il moltiplicatore idrico (5×) configurati globalmente, scorporando i pesi esatti di farina e liquido e mostrando la procedura per la cottura del Roux.
* 🧫 **Modulo Prefermentazione:** Integrazione e scorporo automatico di acqua, farina e lievito per la gestione anticipata di Poolish (100% idro) e Biga (44% idro).
* 📚 **Sezione Wiki Pubblica Unificata:** Nuova rotta `/wiki` ad alto impatto visivo accessibile a tutti gli utenti tramite un pulsante dedicato situato in cima al ricettario. Ospita guide e manuali tecnici pre-caricati senza dipendenze o conflitti di database.
* 🎨 **UI High-Contrast & Leggibilità:** Sfondo del `body` uniformato universalmente sulla palette chiara e riposante `#f8fafc` derivata dall'admin. Scuriti i testi secondari e i titoli del tema *Forno di Paese* per eliminare l'affaticamento visivo.
* 📐 **Centratura Geometrica dei Badge:** Tutti i badge della forza ($W$) e i tag condizionali (es. "TEST") possiedono un layout `inline-flex` che assicura l'allineamento geometrico perfetto del testo sia in verticale che in orizzontale.
* 🔒 **Sicurezza Account Centralizzata:** Rotta dedicata per il cambio password amministratore protetta da hashing crittografico (Werkzeug) direttamente dal pannello di controllo.

---

## 💾 Guida all'Installazione su Server Linux

Per fare in modo che il sito sia sempre attivo e raggiungibile da internet, va installato su un server Linux (es. Ubuntu Server) utilizzando Gunicorn (l'application server) e Systemd (il gestore di servizi di Linux).

### Step 1: Preparazione del Server Linux
Connettiti al tuo server tramite terminale SSH e installa i componenti base richiesti dal sistema:

```bash
sudo apt update
sudo apt install python3-pip python3-venv git -y
Step 2: Scaricamento e Configurazione del Codice
Spostati nella cartella web del server, scarica lo script da GitHub e configura l'ambiente protetto (ambiente virtuale Python):

Bash
cd /var/www
sudo git clone [https://github.com/wifi75/IlMioRicettario.git](https://github.com/wifi75/IlMioRicettario.git)
sudo chown -R $USER:$USER /var/www/IlMioRicettario
cd IlMioRicettario

python3 -m venv venv
source venv/bin/activate
pip install flask flask_sqlalchemy flask_login flask_migrate werkzeug gunicorn
flask db upgrade
deactivate
Step 3: Configurazione del Servizio Automatico (Systemd)
Creiamo un servizio di sistema per fare in modo che Linux mantenga il sito attivo in background e lo riavvii da solo se le server si spegne o si riavvia.

Apri l'editor di testo del server:

Bash
sudo nano /etc/systemd/system/ricettario.service
Incolla dentro il file questo blocco di testo (ricordati di cambiare "tuo_utente" con il vero nome del tuo utente sul server Linux):

Ini, TOML
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
Step 4: Avvio del Sito su Linux
Attiva il servizio appena creato e digitalo come prioritario all'avvio del server:

Bash
sudo systemctl daemon-reload
sudo systemctl enable ricettario
sudo systemctl start ricettario
🖥️ Come Raggiungere il Sito dal Browser
Una volta avviato il servizio su Linux, l'applicazione è attiva e in ascolto sulla porta 8080. Per navigare sul sito dal tuo computer, tablet o smartphone connesso a internet, apri il browser (Chrome, Safari, Edge) e digita nella barra degli indirizzi:

Plaintext
http://IP_DEL_TUO_SERVER:8080
🔐 Guida Completa di Amministrazione (Pannello Admin)
Il sito si divide in due parti: la parte pubblica (il catalogo delle formule accessibile a tutti) e la zona di amministrazione (dove puoi aggiungere ingredienti, modificare coefficienti e creare ricette).

1. Come Entrare nel Pannello di Controllo
Per accedere alla schermata di Login amministrativa, aggiungi /admin/login alla fine del tuo indirizzo web, in questo modo:

Plaintext
http://IP_DEL_TUO_SERVER:8080/admin/login
Ti troverai davanti a una schermata sicura che ti chiederà Nome Utente e Password.

2. Credenziali di Fabbrica (Primo Accesso)
Al primo avvio, lo script genera automaticamente nel database un utente amministratore standard con le seguenti credenziali:

Nome Utente: admin

Password Temporanea: admin123

3. Come Modificare la Password di Amministrazione
Per cambiare la password di amministrazione ed impostarne una tua personale, segui questa procedura guidata direttamente dal pannello:

Accedi al pannello amministrativo.

Clicca sulla voce "Sicurezza Account" nella sidebar di sinistra.

Compila il modulo inserendo la password attuale (admin123) e la nuova chiave personalizzata (minimo 6 caratteri).

Premi "Aggiorna Ora". Il sistema genererà automaticamente il nuovo hash di protezione sicuro (password_hash) memorizzandolo nel database senza mai salvarlo in chiaro.

📊 Comandi Utili per la Gestione del Server
Se effettui modifiche ai file del codice o ai template HTML e vuoi vederle applicate sul sito internet, devi dire a Linux di riavviare l'applicazione in background. Usa questi comandi rapidi:

Controllare se il sito sta girando bene: sudo systemctl status ricettario

Applicare modifiche e riavviare il sito: sudo systemctl restart ricettario

Vedere la lista degli errori in tempo reale: sudo journalctl -u ricettario -f

📈 Sviluppi Futuri della Roadmap (V3)
[ ] Media Ponderata del W: Calcolo automatico della forza finale del mix di farine quando se ne usano diverse nella stessa ricetta.

[ ] Modulo Gestione Lievito Madre: Integrazione del calcolatore per la scomposizione automatica di acqua e farina derivanti dall'utilizzo di colture liquide (LiCoLi) o solide.

⭐️ Progetto ideato, architettato e sviluppato con passione da Tiziano Cassone © 2026.