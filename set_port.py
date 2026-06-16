"""
Il Mio Ricettario — Configurazione porta per il Setup Wizard

Esegui questo script UNA SOLA VOLTA prima del primo avvio,
se la porta di default (8080) è già occupata sul tuo server.

Uso:
    python set_port.py
"""

import os
import sys


def main():
    print()
    print("=" * 52)
    print("  Il Mio Ricettario — Configurazione porta setup")
    print("=" * 52)
    print()
    print("Questo script imposta la porta su cui sarà")
    print("raggiungibile il Setup Wizard al primo avvio.")
    print()

    port_input = input("Inserisci la porta desiderata [8080]: ").strip()

    if not port_input:
        port = 8080
    else:
        try:
            port = int(port_input)
            if not (1024 <= port <= 65535):
                raise ValueError
        except ValueError:
            print()
            print("ERRORE: la porta deve essere un numero tra 1024 e 65535.")
            sys.exit(1)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    instance_dir = os.path.join(base_dir, "instance")
    instance_cfg = os.path.join(instance_dir, "config.py")

    os.makedirs(instance_dir, exist_ok=True)

    with open(instance_cfg, "w", encoding="utf-8") as f:
        f.write(f"PORT = {port}\n")

    print()
    print(f"  OK — instance/config.py creato con PORT = {port}")
    print()
    print("  Passo successivo: avvia il servizio e apri nel browser:")
    print()
    print(f"      http://<indirizzo-server>:{port}/setup")
    print()
    print("  Il wizard completerà la configurazione (Secret Key, ecc.).")
    print("  Dopo il salvataggio riavvia il servizio:")
    print()
    print("      systemctl restart ilmioricettario")
    print()
    print("=" * 52)
    print()


if __name__ == "__main__":
    main()
