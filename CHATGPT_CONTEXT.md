===================================================================
CONTEXT DI PROGETTO: "IL MIO RICETTARIO" (Aggiornato: Giugno 2026)
===================================================================

PROGETTO
- Nome: Il Mio Ricettario
- Sviluppatore Principale: Tiziano Cassone
- Repository GitHub: https://github.com/wifi75/IlMioRicettario

-------------------------------------------------------------------
STACK TECNOLOGICO CORRENTE
-------------------------------------------------------------------
* Python 3
* Flask (Flask-SQLAlchemy, Flask-Login)
* SQLite
* Bootstrap 5 & Bootstrap Icons
* HTML / CSS / JavaScript (Vanilla / Client-side Engine)
* Jinja2
* Quill.js v1.3.6 (Editor WYSIWYG integrato)

-------------------------------------------------------------------
OBIETTIVO ARCHITETTURALE
-------------------------------------------------------------------
Realizzare una piattaforma professionale per la gestione di ricette dinamiche e formule di panificazione basate sulla Percentuale del Fornaio (Baker's Percentage, dove la farina totale rappresenta sempre la base 100%). Ogni ricetta attiva moduli e motori di calcolo configurabili dal backend e ricalcolati in tempo reale nel frontend tramite JavaScript.

-------------------------------------------------------------------
STRUTTURA DEL DATABASE (MODELLI SQLALCHEMY)
-------------------------------------------------------------------
* User: Gestione utenti e credenziali amministrative. Password protette tramite 'password_hash' (autenticazione via Flask-Login).
* MasterIngredient: Anagrafica centralizzata delle materie prime (ID, nome, flag 'is_flour', flag 'is_liquid'). Popolata via seeding automatico in app.py.
* Recipe: Testata della formula (id, name, slug, description, instructions, temp_chiusura, tempo_autolisi, tempo_puntata, tempo_appretto).
* RecipeIngredient: Relazione Many-to-Many tra ricette e ingredienti con l'aggiunta di metadati di calcolo (quantity, unit, is_flour, is_liquid, sort_order).
* RecipeFeature: Flag booleani per attivare/disattivare i singoli moduli e automatismi su ogni specifica ricetta (enable_piece_count, enable_piece_weight, enable_yeast_type, enable_tangzhong, enable_poolish, enable_biga).
* Setting: Parametri globali del sistema (fresh_to_dry_ratio per la conversione dei lieviti, tangzhong_flour_percent, tangzhong_liquid_multiplier).
* WikiArticle: Articoli enciclopedici della sezione Wiki (id, title, slug, content, category).

-------------------------------------------------------------------
LOGICHE OPERATIVE CHIAVE (DA PRESERVARE TASSATIVAMENTE)
-------------------------------------------------------------------

1. REGOLE DI SALVATAGGIO & EDITOR WORD (Quill.js):
   - Nei form di inserimento e modifica ricetta ('recipe_form.html' e 'recipe_edit_form.html') è integrato l'editor Quill.js.
   - Al submit del form, un listener JavaScript cattura il testo dell'editor tramite 'quill.getText().trim()' e lo inietta in un input hidden con name="instructions".
   - Nel database, il campo 'instructions' memorizza il testo lineare mantenendo esclusivamente i caratteri nativi di nuova riga ('\n').

2. ALGORITMO DI PARSING DELLE ISTRUZIONI (Jinja2):
   - Nei file di visualizzazione frontend ('recipe_public_detail.html') e backend ('recipe_detail.html'), il testo delle istruzioni viene elaborato dinamicamente riga per riga tramite Jinja2 (.split('\n')).
   - L'algoritmo genera in automatico un elenco numerato progressivo ordinato (1., 2., 3...).
   - La primissima parola di ogni riga viene isolata e racchiusa automaticamente dentro il tag <strong> (es. "Impasta a velocità..." diventa "<strong>Impasta</strong> a velocità...").

3. ROTTE E DISATTIVAZIONE DASHBOARD:
   - La rotta '/admin/dashboard' è stata permanentemente disattivata e converte le richieste in un redirect sicuro di tipo 302 verso la rotta '/admin/recipes'.
   - La lista centrale delle ricette è il fulcro di gestione dell'intero pannello di amministrazione.

4. PROTEZIONE DEI DATI LOCALI:
   - Il file '.gitignore' esclude tassativamente l'upload su GitHub della cartella 'instance/', dei file con estensione '.db' (database personali) e delle cartelle '__pycache__/' (cache di compilazione Python).

-------------------------------------------------------------------
REGOLE PER LE FUTURE AI IN CHAT (REGOLE TASSATIVE)
-------------------------------------------------------------------
- Fornire SEMPRE codici completi dei file modificati, pronti al copia-incolla diretto. Non usare mai placeholder o commenti di interruzione del codice.
- Mantenere intatta la firma dell'autore nel footer dell'amministrazione (base.html): "Architettato e sviluppato da Tiziano Cassone".
- Non inserire query pesanti o cicliche all'interno di '@app.context_processor'. Tutte le interrogazioni al DB devono essere isolate e veicolate tramite i rispettivi Blueprint.