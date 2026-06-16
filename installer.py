#!/usr/bin/env python3
"""
Il Mio Ricettario — Web Installer
Avvio: python installer.py   (oppure sudo python installer.py per abilitare il servizio)
Browser: http://localhost:5000
"""
import os
import sys
import secrets
import subprocess
from datetime import datetime

from flask import Flask, render_template, request, jsonify

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE_DIR = os.path.join(BASE_DIR, 'instance')
INSTANCE_CFG = os.path.join(INSTANCE_DIR, 'config.py')

installer_app = Flask(__name__, template_folder='templates')
installer_app.secret_key = secrets.token_hex(16)


def _is_configured():
    return os.path.exists(INSTANCE_CFG)


def _is_root():
    try:
        return os.geteuid() == 0
    except AttributeError:
        return False


def _check_requirements():
    errors = []
    if sys.version_info < (3, 9):
        errors.append(f"Python 3.9+ richiesto (versione attuale: {sys.version.split()[0]})")
    for pkg in ['flask', 'flask_sqlalchemy', 'flask_login', 'flask_migrate', 'werkzeug']:
        try:
            __import__(pkg)
        except ImportError:
            errors.append(f"Pacchetto mancante: {pkg} — esegui: pip install -r requirements.txt")
    return errors


@installer_app.route('/')
def index():
    if _is_configured():
        return render_template('installer/already_installed.html', instance_cfg=INSTANCE_CFG)
    req_errors = _check_requirements()
    return render_template('installer/setup.html',
        req_errors=req_errors,
        generated_key=secrets.token_hex(32),
        is_root=_is_root(),
        base_dir=BASE_DIR,
        errors=[],
        form={}
    )


@installer_app.route('/install', methods=['POST'])
def install():
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
        errors.append("La Secret Key deve avere almeno 32 caratteri. Usa il tasto 'Genera' per crearne una sicura.")

    if errors:
        return render_template('installer/setup.html',
            errors=errors,
            req_errors=[],
            form=request.form,
            generated_key=secret_key or secrets.token_hex(32),
            is_root=_is_root(),
            base_dir=BASE_DIR
        )

    os.makedirs(INSTANCE_DIR, exist_ok=True)
    with open(INSTANCE_CFG, 'w', encoding='utf-8') as f:
        f.write(f"# Generato da Il Mio Ricettario Installer — {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write("# Non modificare manualmente — rilancia l'installer per riconfigurare\n\n")
        f.write(f'SECRET_KEY = "{secret_key}"\n')
        f.write(f'PORT = {port}\n')

    venv_python = os.path.join(BASE_DIR, 'venv', 'bin', 'python')
    service_content = (
        "[Unit]\n"
        "Description=Il Mio Ricettario Flask\n"
        "After=network.target\n\n"
        "[Service]\n"
        "User=root\n"
        "Group=root\n"
        f"WorkingDirectory={BASE_DIR}\n"
        f"Environment=\"PATH={BASE_DIR}/venv/bin\"\n"
        f"Environment=\"SECRET_KEY={secret_key}\"\n"
        f"ExecStart={venv_python} {BASE_DIR}/app.py\n"
        "Restart=always\n"
        "RestartSec=5\n\n"
        "[Install]\n"
        "WantedBy=multi-user.target\n"
    )

    service_installed = False
    service_error = None
    service_path = '/etc/systemd/system/ilmioricettario.service'

    if _is_root():
        try:
            with open(service_path, 'w') as f:
                f.write(service_content)
            subprocess.run(['systemctl', 'daemon-reload'], check=True, capture_output=True)
            subprocess.run(['systemctl', 'enable', 'ilmioricettario'], check=True, capture_output=True)
            subprocess.run(['systemctl', 'start', 'ilmioricettario'], check=True, capture_output=True)
            service_installed = True
        except Exception as e:
            service_error = str(e)

    return render_template('installer/success.html',
        port=port,
        service_content=service_content,
        service_installed=service_installed,
        service_error=service_error,
        service_path=service_path,
        is_root=_is_root(),
        base_dir=BASE_DIR
    )


@installer_app.route('/api/generate-key')
def api_generate_key():
    return jsonify({'key': secrets.token_hex(32)})


@installer_app.route('/reset', methods=['POST'])
def reset():
    if os.path.exists(INSTANCE_CFG):
        os.remove(INSTANCE_CFG)
    return jsonify({'ok': True})


if __name__ == '__main__':
    print()
    print("=" * 60)
    print("  Il Mio Ricettario — Web Installer")
    print()
    print("  Apri il browser su:")
    print("  http://localhost:5000")
    print()
    if not _is_root():
        print("  NOTA: per abilitare il servizio systemd automaticamente")
        print("  rilancia con: sudo python installer.py")
    else:
        print("  Avviato come root — il servizio systemd verra'")
        print("  abilitato automaticamente al termine dell'installazione.")
    print("=" * 60)
    print()
    installer_app.run(host='0.0.0.0', port=5000, debug=False)
