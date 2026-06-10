# 📖 Manuale Utente - Il Mio Ricettario (v2.2.0)

Benvenuto nel manuale ufficiale di **Il Mio Ricettario**.

Questa guida descrive il funzionamento dell'applicazione sia dal punto di vista dell'utilizzatore finale che dell'amministratore incaricato della gestione delle formule.

---

# 🌐 1. Accesso all'Applicazione

L'applicazione è disponibile tramite browser web.

## Ambiente di Sviluppo

```text
http://127.0.0.1:8080
```

## Ambiente di Produzione

```text
http://IP_DEL_SERVER:8080
```

La porta predefinita del servizio è:

```text
8080
```

---

# 🍞 2. Catalogo Pubblico delle Ricette

La schermata principale mostra l'elenco delle formule pubblicate.

Ogni ricetta viene rappresentata tramite una card contenente:

* immagine di copertina;
* nome formula;
* descrizione;
* pulsante di accesso al calcolatore.

---

# 📚 3. Wiki Tecnica Pubblica

Nella parte superiore della home page è disponibile il pulsante:

```text
Esplora la Wiki & Linee Guida Tecniche
```

La Wiki è accessibile tramite:

```text
/wiki
```

e contiene:

* tecniche di panificazione;
* guide operative;
* documentazione dell'arte bianca;
* materiale di approfondimento.

---

# 🧮 4. Calcolatore Dinamico delle Formule

Entrando in una ricetta si accede al simulatore professionale.

Il sistema ricalcola automaticamente:

* grammature;
* idratazione;
* lieviti;
* pezzature;
* teglie;
* prefermenti.

---

## Gestione Pezzature

L'utente può:

* impostare il numero dei panetti;
* definire il peso del singolo pezzo;
* ottenere il nuovo totale impasto.

---

## Gestione Teglie

Se la ricetta possiede teglie associate:

* vengono mostrate automaticamente;
* è possibile aumentare o diminuire le quantità;
* il sistema ricalcola l'impasto necessario.

---

## Conversione Lieviti

Supporto per:

* lievito fresco;
* lievito secco.

La conversione viene effettuata automaticamente utilizzando il rapporto definito nelle impostazioni globali.

---

## Idratazione Dinamica

Quando abilitata dalla ricetta:

* l'idratazione può essere modificata tramite slider;
* acqua e percentuali vengono aggiornate in tempo reale.

---

## Visualizzazione Forza Farine (W)

Le farine mostrano un badge dedicato contenente il valore:

```text
W
```

Gli ingredienti non classificati come farine non mostrano alcun badge.

---

# 🥣 5. Tangzhong

Se la ricetta utilizza il modulo Tangzhong:

* il sistema isola automaticamente una quota di farina;
* viene calcolata la quantità di liquido necessaria;
* viene mostrata la procedura di preparazione.

---

# 🧫 6. Poolish e Biga

Il sistema supporta:

## Poolish

* idratazione 100%.

## Biga

* idratazione 44%.

Le quantità vengono automaticamente separate dal totale impasto.

---

# 🔐 7. Accesso all'Area Amministrativa

Per accedere al pannello di controllo:

```text
http://IP_DEL_SERVER:8080/admin/login
```

Inserire:

* nome utente;
* password.

Una volta autenticati si accede al pannello amministrativo.

---

# ⚙️ 8. Gestione Ricette

La sezione più importante del sistema.

Permette:

* creazione formule;
* modifica formule;
* eliminazione formule;
* gestione ingredienti;
* gestione immagini;
* configurazione moduli.

---

## Editor Istruzioni (Quill.js)

Le istruzioni vengono inserite tramite editor visuale.

Funzioni principali:

* testo formattato;
* paragrafi;
* elenchi;
* allineamenti.

Al salvataggio il contenuto viene trasferito automaticamente al database.

---

## Gestione Ingredienti

Durante la compilazione della ricetta:

* gli ingredienti vengono selezionati dall'anagrafica centrale;
* il sistema recupera automaticamente il valore W;
* i dati vengono storicizzati nella formula.

---

## Gestione Teglie

È possibile associare una o più teglie ad una singola ricetta.

Le teglie vengono selezionate dalla flotta globale.

---

# 🖼️ 9. Libreria Immagini Centralizzata (Novità v2.2.0)

La gestione immagini è stata completamente riprogettata.

---

## Archivio Centrale

Le immagini vengono archiviate una sola volta tramite:

```text
MasterImage
```

e possono essere riutilizzate da più ricette.

---

## Associazione Immagine

Nel form della ricetta è presente un selettore dedicato.

Procedura:

1. Aprire il menu a tendina.
2. Selezionare l'immagine desiderata.
3. Premere:

```text
✓ Applica
```

4. Salvare la ricetta.

---

## Anteprima Dinamica

Dopo la selezione:

* compare immediatamente l'anteprima;
* viene mostrata la miniatura;
* l'associazione viene mantenuta dopo il salvataggio.

---

## Scollegamento Immagine

Per rimuovere l'immagine:

1. Aprire la ricetta.
2. Premere:

```text
Scollega Immagine
```

3. Salvare.

---

# 🧾 10. Gestione Ingredienti (Master Ingredienti)

Archivio globale degli ingredienti.

Campi principali:

* Nome;
* È una Farina;
* È un Liquido;
* Valore W.

---

## Regola di Sicurezza

Un ingrediente non può essere contemporaneamente:

* farina;
* liquido.

Il controllo viene eseguito automaticamente tramite JavaScript.

---

# 🍕 11. Gestione Teglie (Master Bakery Pan)

Archivio globale delle teglie.

Ogni elemento possiede:

* nome;
* tipologia;
* capacità in grammi.

---

# 🎨 12. Impostazioni Globali

Permettono di configurare:

* nome sito;
* descrizione sito;
* rapporto lieviti;
* parametri Tangzhong;
* tema grafico.

---

# 🔒 13. Sicurezza Account

Permette di modificare:

* password amministrativa;
* credenziali di accesso.

Le password vengono salvate esclusivamente tramite hash crittografico.

---

# 💡 Buone Pratiche

Per ottenere il massimo dal sistema:

1. Utilizzare immagini con sfondo chiaro.
2. Mantenere descrizioni brevi.
3. Verificare sempre i flag Farina/Liquido.
4. Utilizzare nomi ricetta coerenti.
5. Aggiornare regolarmente la libreria ingredienti.

---

# 👨‍💻 Credits

Architettato e sviluppato da Tiziano Cassone.

© 2026 - Il Mio Ricettario
