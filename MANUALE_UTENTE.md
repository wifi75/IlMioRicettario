# 📖 Manuale Utente - Il Mio Ricettario (v3.0.0)

Benvenuto in **Il Mio Ricettario**, la piattaforma professionale per la gestione di ricette di panificazione, pizza, focaccia, grandi lievitati e arte bianca.

Questo manuale descrive tutte le funzionalità disponibili sia per l'utente che consulta le ricette sia per l'amministratore che gestisce il catalogo.

---

# 🌐 1. Accesso all'Applicazione

L'applicazione è accessibile tramite qualsiasi browser moderno:

* Google Chrome
* Microsoft Edge
* Firefox
* Safari

## Ambiente di Sviluppo

```text
http://127.0.0.1:8080
```

## Ambiente di Produzione

```text
http://INDIRIZZO_SERVER
```

---

# 🍞 2. Catalogo Ricette

La pagina principale mostra tutte le ricette pubblicate.

Ogni ricetta presenta:

* immagine di copertina;
* nome della ricetta;
* descrizione;
* accesso al dettaglio completo.

Le ricette non pubblicate non sono visibili agli utenti.

---

# 📋 3. Scheda Ricetta

Aprendo una ricetta vengono visualizzate:

* descrizione;
* ingredienti;
* procedimento;
* immagini;
* tempi di lavorazione;
* prefermenti;
* strumenti associati.

Tutte le informazioni vengono mostrate in modo ottimizzato sia su desktop che su smartphone.

---

# 🧮 4. Calcolatore Dinamico

Una delle funzionalità principali del sistema.

Il calcolatore consente di adattare automaticamente la formula a nuove esigenze produttive.

È possibile:

* aumentare le quantità;
* diminuire le quantità;
* modificare il peso totale impasto;
* modificare il numero di pezzi;
* adattare la ricetta a diverse teglie.

---

## Peso Totale Impasto

Il sistema utilizza sempre il peso reale della ricetta salvata.

La formula originale non viene modificata.

Qualsiasi variazione effettuata dall'utente è temporanea e utilizzata esclusivamente per il calcolo.

---

## Gestione Pezzature

È possibile specificare:

* numero di panetti;
* peso del singolo panetto.

Il sistema ricalcola automaticamente tutti gli ingredienti mantenendo invariati i rapporti della ricetta originale.

### Esempio

Ricetta originale:

```text
4 panetti da 250 g
```

Nuova richiesta:

```text
8 panetti da 280 g
```

Tutti gli ingredienti verranno aggiornati automaticamente.

---

## Gestione Teglie

Se la ricetta dispone di teglie associate, è possibile:

* selezionare la teglia desiderata;
* indicare il numero di teglie;
* ottenere il nuovo peso impasto necessario.

Il sistema esegue il calcolo automaticamente.

---

# 💧 5. Idratazione

Le ricette che prevedono il controllo dell'idratazione consentono di:

* visualizzare la percentuale totale;
* modificare il livello di idratazione;
* aggiornare automaticamente la quantità di acqua.

Tutti i valori vengono ricalcolati in tempo reale.

---

# 🧫 6. Prefermenti

Il sistema supporta diverse tecniche di prefermentazione.

---

## Poolish

Caratteristiche:

* idratazione 100%;
* sviluppo aromatico;
* maggiore estensibilità.

---

## Biga

Caratteristiche:

* idratazione 44%;
* maggiore struttura;
* migliore conservabilità.

---

## Tangzhong

Quando presente:

* viene indicata la quantità di farina dedicata;
* viene indicata la quantità di liquido necessaria;
* viene mostrata la procedura di preparazione.

---

# 🧂 7. Ingredienti

Ogni ingrediente può contenere informazioni aggiuntive.

Per le farine viene visualizzato il valore:

```text
W
```

che rappresenta la forza della farina.

---

# 📚 8. Wiki Tecnica

La piattaforma include una Wiki dedicata all'arte bianca.

Accesso:

```text
/wiki
```

Contenuti disponibili:

* tecniche di impasto;
* lievitazione;
* fermentazione;
* utilizzo dei prefermenti;
* gestione delle farine;
* procedure operative.

---

# 🛠️ 9. Installazione Guidata (Web Installer)

L'applicazione include un wizard di installazione accessibile via browser.

Avvio:

```bash
python installer.py
# oppure, per abilitare il servizio systemd in automatico:
sudo python installer.py
```

Aprire il browser su:

```text
http://localhost:5000
```

Il wizard guida l'utente nella configurazione di:

* porta dell'applicazione
* Secret Key crittografica (generata automaticamente)

Al termine genera il file `instance/config.py` che non viene mai incluso in Git, eliminando i conflitti tra aggiornamenti e configurazioni locali.

Se avviato come root, il servizio systemd viene creato, abilitato e avviato in automatico. Altrimenti viene mostrato il contenuto del file `.service` da copiare manualmente.

---

# 🗄️ 10. Backup e Ripristino

Il pannello di backup è accessibile da:

```text
Admin → Manutenzione → Backup e Ripristino
```

## Export disponibili

* **Esporta Ricette** — tutte le ricette con ingredienti e moduli attivi, formato `.json`
* **Esporta Configurazione** — impostazioni, ingredienti, teglie e wiki, formato `.json`
* **Backup Completo** — ricette, configurazione e immagini caricate, formato `.zip`

## Import

1. Selezionare il file `.json` o `.zip` da ripristinare.
2. Scegliere la modalità:
   * **Merge** — aggiunge solo i dati non presenti, preserva quelli esistenti.
   * **Replace** — elimina prima i dati esistenti, poi importa. Operazione irreversibile.
3. Premere **Avvia Ripristino**.

---

# 🔐 11. Accesso Area Amministrativa

L'accesso amministrativo è protetto da autenticazione.

Percorso:

```text
/admin/login
```

Inserire:

* nome utente;
* password.

Solo gli utenti autorizzati possono accedere al backend.

Alla prima installazione il sistema genera automaticamente una password sicura e la mostra una sola volta via console. Cambiare immediatamente la password dal pannello:

```text
/admin/change_password
```

---

# ⚙️ 12. Gestione Ricette

Dal pannello amministrativo è possibile:

* creare nuove ricette;
* modificare ricette esistenti;
* eliminare ricette;
* pubblicare o nascondere ricette.

---

## Editor Procedimento

Le istruzioni vengono inserite tramite editor visuale.

Funzionalità disponibili:

* grassetto;
* corsivo;
* elenchi;
* titoli;
* paragrafi;
* immagini.

Il contenuto viene automaticamente ottimizzato e salvato nel database.

---

# 🖼️ 13. Libreria Immagini Centralizzata

Le immagini vengono gestite da un archivio unico.

Vantaggi:

* caricamento una sola volta;
* riutilizzo su più ricette;
* gestione centralizzata;
* anteprima immediata.

---

## Associare un'Immagine

1. Aprire la ricetta.
2. Selezionare l'immagine dal menu.
3. Premere "Applica".
4. Salvare la ricetta.

---

## Rimuovere un'Immagine

1. Aprire la ricetta.
2. Premere "Scollega Immagine".
3. Salvare.

---

# 🥣 14. Gestione Ingredienti

L'archivio ingredienti centralizzato consente di definire:

* nome ingrediente;
* tipologia;
* valore W;
* classificazione farina;
* classificazione liquido.

---

# 🍕 15. Gestione Teglie

L'archivio teglie permette di registrare:

* nome;
* tipologia;
* capacità impasto.

Le teglie possono essere associate a più ricette.

---

# 🎨 16. Impostazioni Globali

Le impostazioni consentono di configurare:

* nome del sito;
* descrizione del sito;
* tema grafico;
* parametri Tangzhong;
* rapporto lievito fresco/secco.

---

# 🔒 17. Sicurezza

Le password vengono memorizzate esclusivamente tramite hash crittografico (bcrypt).

Il sistema non conserva password in chiaro.

## Chiave di Sessione (SECRET_KEY)

L'applicazione richiede una variabile d'ambiente `SECRET_KEY` per firmare i cookie di sessione.

Questa chiave è completamente separata dalla password amministratore e non viene mai salvata nel database.

## Password Amministratore

Alla prima installazione il sistema genera automaticamente una password sicura a 16 caratteri e la mostra in console.

Cambiare sempre la password subito dopo la prima installazione:

```text
/admin/change_password
```

## Buone Pratiche

* Non condividere mai la password di accesso.
* Cambiare la password periodicamente.
* Non accedere al pannello da reti pubbliche non sicure.

---

# 🧹 18. Cache del Browser

Dopo aggiornamenti importanti dell'applicazione può essere utile aggiornare la pagina con:

```text
CTRL + F5
```

per forzare il caricamento delle nuove risorse.

---

# 💡 Buone Pratiche

Per ottenere il massimo dal sistema:

1. Utilizzare immagini di buona qualità.
2. Compilare sempre le descrizioni.
3. Mantenere aggiornata l'anagrafica ingredienti.
4. Verificare i valori W delle farine.
5. Salvare frequentemente durante la modifica delle ricette.

---

# 👨‍💻 Credits

Architettato e sviluppato da **Tiziano Cassone**.

© 2026 - Il Mio Ricettario
