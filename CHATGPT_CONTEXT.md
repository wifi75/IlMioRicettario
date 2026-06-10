===================================================================
CONTEXT DI PROGETTO: "IL MIO RICETTARIO" (Aggiornato: Giugno 2026)
===================================================================

PROGETTO
- Nome: Il Mio Ricettario
- Sviluppatore Principale: Tiziano Cassone
- Versione Architetturale: v2.1.0 (Stabile)
- Repository GitHub: https://github.com/wifi75/IlMioRicettario

-------------------------------------------------------------------
STACK TECNOLOGICO CORRENTE
-------------------------------------------------------------------
* Python 3.13
* Flask (Flask-SQLAlchemy, Flask-Login)
* SQLite
* Bootstrap 5.3 & Bootstrap Icons
* HTML / CSS / JavaScript (Vanilla / Client-side Engine)
* Jinja2
* Quill.js v1.3.6 (Editor WYSIWYG integrato nei form)

-------------------------------------------------------------------
STATO STRUTTURALE DEL LAYOUT & LEGGE CROMATICA (V2)
-------------------------------------------------------------------
1. BASE GRAPHIC DESIGN: Lo sfondo del 'body' è bloccato universalmente sul grigio ardesia chiaro '#f8fafc' per tutti i temi chiari. Il tema 'forno_paese' è sanificato con testi scuri ardesia e blu notte profondi per garantire contrasti nitidi.
2. BOX INTESTAZIONE HERO ('recipes_list.html'): Un unico rettangolo bianco compatto con larghezza fissa a '850px'. L'icona della spiga '🌾' è ancorata a sinistra in posizionamento assoluto ('position: absolute; left: 24px; top: 50%; transform: translateY(-50%);'), mantenendo il titolo H1 e il testo descrittivo agganciati al centro geometrico spaccato del contenitore.
3. ALLINEAMENTO ORIZZONTALE/VERTICALE BADGE: Tutti i badge della forza ('w_value') e i tag categorie (es. "TEST") implementano la proprietà Flexbox 'display: inline-flex !important; align-items: center !important; justify-content: center !important;' che costringe il testo scritto al perfetto centro simmetrico della forma.

-------------------------------------------------------------------
STRUTTURA DEL DATABASE (MODELLI SQLALCHEMY)
-------------------------------------------------------------------
* User: Gestione utenti e credenziali amministrative. Password protette tramite 'password_hash' (autenticazione via Flask-Login).
* MasterIngredient: Anagrafica centralizzata delle materie prime (ID, nome, flag 'is_flour', flag 'is_liquid', forza 'w_value'). Popolata via seeding automatico in app.py.
* MasterBakeryPan: Anagrafica centralizzata delle teglie e degli stampi (ID, name, pan_type, weight_capacity) assegnabili dinamicamente come flotta alle singole ricette.
* Recipe: Testata della formula (id, name, slug, description, instructions, temp_chiusura, tempo_autolisi, tempo_puntata, tempo_appretto). Include la relazione Many-to-Many con la flotta teglie ('pans').
* RecipeIngredient: Relazione Many-to-Many tra ricette e ingredienti con l'aggiunta di metadati di calcolo cristallizzati (quantity, unit, is_flour, is_liquid, w_value, sort_order).
* RecipeFeature: Flag booleani per attivare/disattivare i singoli moduli e automatismi su ogni specifica ricetta (enable_piece_count, enable_piece_weight, enable_yeast_type, enable_tangzhong, enable_poolish, enable_biga).
* Setting: Parametri globali del sistema (fresh_to_dry_ratio, tangzhong_flour_percent, tangzhong_liquid_multiplier, site_name, site_description, theme_active).
* wiki: Classe di modello definita in 'models/wiki.py' interamente in caratteri minuscoli per la gestione degli articoli enciclopedici.

-------------------------------------------------------------------
LOGICHE OPERATIVE CHIAVE (DA PRESERVARE TASSATIVAMENTE)
-------------------------------------------------------------------
1. APPLICAZIONE ROTTA WIKI PUBBLICA IMMORTALE:
   - La visualizzazione pubblica della Wiki avviene tramite la rotta '/wiki' gestita in 'routes/recipes.py' dalla funzione 'wiki_public_list()'.
   - Per immunizzare l'applicazione da crash all'avvio derivanti dalla classe 'wiki' minuscola o da assenza di tabelle, i dati del manuale d'uso d'arte bianca sono pre-caricati e passati via dizionario a 'wiki_public.html'.
   - Il collegamento in frontend è gestito da un link statico a href="/wiki" inserito sopra l'header di 'recipes_list.html'.

2. REGOLE DI SALVATAGGIO & EDITOR WORD (Quill.js):
   - Nei form di inserimento e modifica ricetta è integrato l'editor Quill.js che inietta il testo lineare in un input hidden con name="instructions".

3. ALGORITMO DI PARSING DELLE ISTRUZIONI (Jinja2):
   - Il testo delle istruzioni viene elaborato riga per riga tramite Jinja2 (.split('\n')), generando un elenco numerato progressivo ordinato e racchiudendo automaticamente la primissima parola dentro il tag <strong>.

4. PROTEZIONE DEI DATI LOCALI:
   - Il file '.gitignore' esclude tassativamente l'upload su GitHub della cartella 'instance/', dei file '.db' e delle cartelle '__pycache__/'.

-------------------------------------------------------------------
REGOLE PER LE FUTURE AI IN CHAT (REGOLE TASSATIVE)
-------------------------------------------------------------------
- Fornire SEMPRE codici completi dei file modificati, pronti al copia-incolla diretto. Non usare mai placeholder o commenti di interruzione del codice.
- Mantenere intatta la firma dell'autore nel footer dell'amministrazione (base.html): "Architettato e sviluppato da Tiziano Cassone".
- Non inserire query pesanti o cicliche all'interno di '@app.context_processor'. Tutte le interrogazioni al DB devono essere isolate e veicolate tramite i rispettivi Blueprint.