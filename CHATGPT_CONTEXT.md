# CHATGPT CONTEXT

Contesto del progetto Il Mio Ricettario.

# PROGETTO: Il Mio Ricettario

Sto sviluppando un nuovo progetto chiamato "Il Mio Ricettario".

Repository GitHub:
https://github.com/wifi75/IlMioRicettario

Stack tecnologico:

* Python 3
* Flask
* SQLite
* Bootstrap 5
* HTML
* CSS
* JavaScript
* Jinja2

Obiettivo:

Realizzare una piattaforma professionale per la gestione di ricette dinamiche.

Non è un semplice ricettario.

Ogni ricetta può attivare moduli e motori di calcolo configurabili dal backend.

Moduli previsti:

* Numero pezzi
* Peso pezzo
* Teglie
* Formati teglia
* Tipo lievito
* Tangzhong

Esempio:

Una ricetta di panini può consentire:

* scelta numero panini
* scelta peso panino
* scelta tipo lievito

Una ricetta di focaccia può consentire:

* scelta numero teglie
* scelta formato teglia
* scelta tipo lievito

Motore lievito:

L'utente può scegliere nel frontend:

* Lievito fresco
* Lievito secco Caputo

La conversione deve essere configurabile dal backend tramite impostazioni globali.

Motore Tangzhong:

Parametri configurabili dal backend:

* percentuale farina
* moltiplicatore liquido

Esempio standard:

5% farina
5× latte

Quando il Tangzhong è attivato il sistema deve:

* calcolare automaticamente Tangzhong
* sottrarre farina e latte dagli ingredienti principali
* mostrare una sezione dedicata Tangzhong

Wiki integrata:

Menu Wiki con articoli gestibili dal backend.

Esempi:

* Lievito fresco
* Lievito secco
* Tangzhong
* Poolish
* Biga
* Idratazione

Database previsto:

users

recipes

recipe_ingredients

recipe_features

recipe_trays

settings

wiki_articles

Regole fondamentali:

1. Fornire sempre file completi.
2. Non fornire patch parziali.
3. Non rompere funzionalità esistenti.
4. Indicare sempre il file da modificare.
5. Se si modifica app.py indicare sempre la sezione corretta.
6. Architettura semplice e facilmente manutenibile.
7. Il backend deve poter abilitare/disabilitare i moduli per ogni ricetta.

Stato attuale:

* cartella progetto creata
* repository GitHub creato
* primo commit eseguito
* struttura iniziale pronta

Voglio procedere con la V1 professionale partendo da:

* database
* login amministratore
* dashboard admin
* gestione ricette
* moduli dinamici
