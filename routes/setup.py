import os
import secrets
from datetime import datetime

from flask import Blueprint, render_template, request, jsonify

setup_bp = Blueprint('setup', __name__)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
INSTANCE_DIR = os.path.join(BASE_DIR, 'instance')
INSTANCE_CFG = os.path.join(INSTANCE_DIR, 'config.py')


@setup_bp.route('/setup', methods=['GET'])
def wizard():
    return render_template('setup/wizard.html',
        generated_key=secrets.token_hex(32),
        errors=[],
        form={}
    )


@setup_bp.route('/setup', methods=['POST'])
def wizard_save():
    port_raw = request.form.get('port', '8080').strip()
    secret_key = request.form.get('secret_key', '').strip()

    errors = []
    try:
        port = int(port_raw)
        if port < 1024 or port > 65535:
            errors.append("La porta deve essere compresa tra 1024 e 65535.")
    except ValueError:
        port = 8080
        errors.append("La porta deve essere un numero intero valido.")

    if not secret_key or len(secret_key) < 32:
        errors.append("La Secret Key deve avere almeno 32 caratteri. Usa il tasto Genera.")

    if errors:
        return render_template('setup/wizard.html',
            errors=errors,
            form=request.form,
            generated_key=secret_key or secrets.token_hex(32)
        )

    os.makedirs(INSTANCE_DIR, exist_ok=True)
    with open(INSTANCE_CFG, 'w', encoding='utf-8') as f:
        f.write(f"# Il Mio Ricettario — configurazione generata il {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write("# Questo file non è mai incluso in git.\n\n")
        f.write(f'SECRET_KEY = "{secret_key}"\n')
        f.write(f'PORT = {port}\n')

    return render_template('setup/complete.html', port=port, base_dir=BASE_DIR)


@setup_bp.route('/setup/generate-key')
def generate_key():
    return jsonify({'key': secrets.token_hex(32)})


@setup_bp.route('/', defaults={'path': ''})
@setup_bp.route('/<path:path>')
def catch_all(path):
    from flask import redirect, url_for
    return redirect(url_for('setup.wizard'))
