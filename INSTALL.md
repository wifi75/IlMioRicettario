# Guida all'Installazione — Il Mio Ricettario

Guida completa per installare e configurare **Il Mio Ricettario** su un server Linux con Ubuntu/Debian.

Tutti i comandi sono pronti per il copia-incolla.

---

## Requisiti

- Server Linux (Ubuntu 20.04+ / Debian 11+)
- Python 3.10 o superiore
- Accesso root o sudo
- Porta libera sul server (default: 8080)

---

## PASSO 1 — Installa le dipendenze di sistema

```bash
apt update && apt install -y python3 python3-venv python3-pip git
```

---

## PASSO 2 — Clona il repository

```bash
cd /var/www
git clone https://github.com/wifi75/IlMioRicettario.git
cd IlMioRicettario
```

---

## PASSO 3 — Crea l'ambiente virtuale e installa i pacchetti Python

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## PASSO 4 — Configura il servizio systemd

Copia il file di esempio incluso nel repository:

```bash
cp ilmioricettario.service.example /etc/systemd/system/ilmioricettario.service
```

Apri il file e adatta il percorso se necessario (default: `/var/www/IlMioRicettario`):

```bash
nano /etc/systemd/system/ilmioricettario.service
```

Contenuto del file (modifica solo `WorkingDirectory` e `User` se il percorso è diverso):

```ini
[Unit]
Description=Il Mio Ricettario — Professional Baking Suite
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/IlMioRicettario
ExecStart=/var/www/IlMioRicettario/venv/bin/python app.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

---

## PASSO 5 — (Solo se la porta 8080 è già in uso) Imposta una porta alternativa

> Salta questo passo se la porta 8080 è libera sul tuo server.

Se la porta 8080 è occupata da un altro servizio, esegui questo script per impostarne una diversa:

```bash
python set_port.py
```

Lo script chiede la porta desiderata (es. 8100) e crea automaticamente `instance/config.py`.
Output atteso:

```
Inserisci la porta desiderata [8080]: 8100

  OK — instance/config.py creato con PORT = 8100

  Passo successivo: avvia il servizio e apri nel browser:

      http://<indirizzo-server>:8100/setup
```

---

## PASSO 6 — Abilita e avvia il servizio

```bash
systemctl daemon-reload
systemctl enable ilmioricettario
systemctl start ilmioricettario
```

Verifica che il servizio sia attivo:

```bash
systemctl status ilmioricettario
```

Output atteso (riga `Active`):

```
Active: active (running) since ...
```

---

## PASSO 7 — Completa la configurazione via browser (Setup Wizard)

Apri nel browser:

```
http://<indirizzo-server>:8080/setup
```

> Se hai scelto una porta diversa al Passo 5, usa quella porta al posto di 8080.

Il wizard chiede:

1. **Porta** — la porta su cui sarà raggiungibile il sito (es. 8100)
2. **Secret Key** — clicca **Genera** per creare automaticamente una chiave sicura

Clicca **Salva Configurazione**. La pagina di conferma mostra il comando per riavviare il servizio.

---

## PASSO 8 — Riavvia il servizio

```bash
systemctl restart ilmioricettario
```

---

## PASSO 9 — Recupera la password amministratore

La password admin viene generata automaticamente al primo avvio e stampata nei log del servizio.

Leggila con:

```bash
journalctl -u ilmioricettario -n 50 --no-pager
```

Cerca la riga:

```
Password: xxxxxxxxxxxxxxxx
```

> Accedi al pannello admin e cambia subito la password da:
> **Admin → Account → Sicurezza e Password**

---

## PASSO 10 — Accedi al pannello di amministrazione

```
http://<indirizzo-server>:<porta>/admin
```

Username: `admin`
Password: quella trovata nei log al Passo 9

---

## Aggiornamento dell'applicazione

Quando viene rilasciata una nuova versione, aggiorna con:

```bash
cd /var/www/IlMioRicettario
git pull origin main
systemctl restart ilmioricettario
```

> `instance/config.py` non è mai incluso in git: `git pull` non sovrascrive mai la tua porta o la tua Secret Key.

Aggiorna i pacchetti Python solo se `requirements.txt` è cambiato:

```bash
source venv/bin/activate
pip install -r requirements.txt
```

---

## Comandi utili

### Log in tempo reale

```bash
journalctl -u ilmioricettario -f
```

### Ultimi 100 log

```bash
journalctl -u ilmioricettario -n 100 --no-pager
```

### Riavvio

```bash
systemctl restart ilmioricettario
```

### Stop

```bash
systemctl stop ilmioricettario
```

### Stato

```bash
systemctl status ilmioricettario
```

---

## Cambiare la porta dopo l'installazione

Puoi cambiare la porta in qualsiasi momento dal pannello admin:

```
Admin → Sistema → Porta Applicazione
```

Inserisci la nuova porta, salva, poi riavvia il servizio:

```bash
systemctl restart ilmioricettario
```

---

## Risoluzione problemi

### Il servizio non parte

Leggi i log per capire il problema:

```bash
journalctl -xeu ilmioricettario
```

### Porta già in uso

Scopri quale processo usa la porta:

```bash
ss -tlnp | grep 8080
```

Poi scegli una porta alternativa con `python set_port.py` e riavvia.

### Reset completo della configurazione

```bash
rm /var/www/IlMioRicettario/instance/config.py
systemctl restart ilmioricettario
```

L'app torna in modalità setup. Apri `/setup` nel browser per riconfigurare.

> Attenzione: questo non cancella il database né le ricette.

---

## Struttura file di configurazione

```
/var/www/IlMioRicettario/
├── instance/
│   └── config.py          ← generato dal wizard, MAI in git
├── data/
│   └── database.db        ← database SQLite, MAI in git
├── static/uploads/        ← immagini caricate
├── ilmioricettario.service.example
├── set_port.py
└── app.py
```

---

*Guida aggiornata alla versione v3.0.2*
