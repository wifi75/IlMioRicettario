# CHATGPT CONTEXT

## PROGETTO

Il Mio Ricettario

Repository GitHub:

https://github.com/wifi75/IlMioRicettario

---

## STACK TECNOLOGICO

* Python 3
* Flask
* SQLite
* Bootstrap 5
* HTML
* CSS
* JavaScript
* Jinja2

---

## OBIETTIVO

Realizzare una piattaforma professionale per la gestione di ricette dinamiche.

Il sistema non deve essere un semplice ricettario.

Ogni ricetta deve poter attivare motori di calcolo e moduli configurabili dal backend.

---

## ARCHITETTURA

Ogni ricetta può abilitare o disabilitare funzionalità specifiche.

Esempi:

### Panini

* Numero panini
* Peso panino
* Tipo lievito

### Focacce

* Numero teglie
* Formato teglia
* Tipo lievito

### Pane in cassetta

* Formato stampo
* Numero stampi
* Tipo lievito
* Tangzhong

---

## MODULI PREVISTI

### Panetti

Permette di scegliere:

* Numero pezzi
* Peso pezzo

### Teglie

Permette di scegliere:

* Numero teglie
* Formato teglia

### Lievito

Permette di scegliere:

* Lievito fresco
* Lievito secco Caputo

La conversione deve essere configurabile dal backend.

### Tangzhong

Configurabile da backend:

* Percentuale farina
* Moltiplicatore liquido

Valori standard:

* 5%
* 5×

Quando attivato il sistema deve:

* calcolare automaticamente il Tangzhong
* sottrarre farina e liquido dalla ricetta principale
* mostrare una sezione dedicata

---

## WIKI

Sezione Wiki integrata.

Argomenti previsti:

* Lievito fresco
* Lievito secco
* Tangzhong
* Poolish
* Biga
* Idratazione

Gestione completa dal backend.

---

## DATABASE

Tabelle principali:

* users
* recipes
* recipe_ingredients
* recipe_features
* recipe_parameters
* recipe_trays
* settings
* wiki_articles

---

## REGOLE DI SVILUPPO

1. Fornire sempre file completi.
2. Non fornire patch parziali.
3. Non rompere funzionalità esistenti.
4. Indicare sempre il file da modificare.
5. Se si modifica app.py indicare la sezione esatta.
6. Architettura semplice e manutenibile.
7. Backend in grado di attivare/disattivare i moduli per ogni ricetta.
8. Mobile First.
9. Compatibilità Smartphone / Tablet / Desktop.
10. Bootstrap 5 come framework UI principale.

---

## STATO ATTUALE

Completato:

* Login amministratore
* Dashboard amministrazione
* Gestione ricette
* Gestione ingredienti
* Calcolo farine totali
* Calcolo liquidi totali
* Calcolo idratazione
* RecipeFeature
* RecipeParameter
* Setting
* SQLite

---

## ROADMAP V1

### Backend

* Gestione Feature Ricetta
* Gestione Parametri Ricetta
* Gestione Wiki
* Gestione Impostazioni Globali

### Motori

* Numero panetti
* Peso panetto
* Idratazione variabile
* Conversione lievito
* Tangzhong
* Poolish
* Biga
* Lievito madre

### Frontend

* Ricette dinamiche
* Moduli generati automaticamente
* Calcolo in tempo reale
* Layout responsive professionale
