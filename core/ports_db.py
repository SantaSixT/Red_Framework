# ==========================================
# BASE DE DONNÉES DES PORTS (Red Team Arsenal)
# ==========================================

TOP_PORTS = {
    # --- Protocoles Standards & Historiques ---
    20: "FTP-DATA", 
    21: "FTP (Transfert de fichiers)", 
    22: "SSH (Secure Shell)", 
    23: "Telnet (Non sécurisé !)",
    25: "SMTP (Mail Routing)", 
    53: "DNS (Résolution de noms)", 
    69: "TFTP (Trivial FTP - UDP/TCP)",
    110: "POP3 (Mail Client)",
    111: "RPCBind (Mappage de ports RPC)", 
    135: "MSRPC (Windows RPC - Critique)", 
    139: "NetBIOS (Partage Windows ancien)", 
    143: "IMAP (Mail Client)",
    161: "SNMP (Supervision - Souvent vulnérable)",
    389: "LDAP (Annuaire Active Directory)",
    445: "SMB (Partage Windows - Vecteur EternalBlue/Ransomware)", 
    465: "SMTPS (Mail Sécurisé)", 
    514: "Syslog (Journaux système)",
    587: "SMTP (Mail Submission)", 
    636: "LDAPS (LDAP Sécurisé)",
    873: "Rsync (Synchronisation de fichiers)",
    993: "IMAPS (IMAP Sécurisé)", 
    995: "POP3S (POP3 Sécurisé)",

    # --- Web & Proxies ---
    80: "HTTP (Web Clair)", 
    443: "HTTPS (Web Sécurisé)", 
    1080: "SOCKS Proxy", 
    3128: "Squid Proxy", 
    8000: "HTTP-Alt (Serveur de dev courant)", 
    8080: "HTTP-Proxy / Tomcat / Jenkins",
    8443: "HTTPS-Alt / Plesk", 
    8888: "HTTP-Alt / Jupyter Notebook",

    # --- Accès Distant & Administration ---
    2049: "NFS (Partage de fichiers Linux)", 
    2082: "cPanel (Administration Web)",
    2083: "cPanel (Sécurisé)",
    2086: "WHM (Web Host Manager)",
    2087: "WHM (Sécurisé)",
    3389: "RDP (Bureau à Distance Windows)",
    5900: "VNC (Contrôle à distance)", 
    5901: "VNC (Écran 1)",
    10000: "Webmin (Administration Linux)",

    # --- Bases de Données (SQL & NoSQL) ---
    1433: "MSSQL (Microsoft SQL Server)",
    1521: "Oracle DB",
    3306: "MySQL / MariaDB", 
    5432: "PostgreSQL", 
    5984: "CouchDB",
    6379: "Redis (Cache en mémoire - Souvent sans mot de passe)",
    7474: "Neo4j (Base de graphes)",
    9200: "Elasticsearch (API REST - Fuites de données massives)",
    9300: "Elasticsearch (Cluster)",
    11211: "Memcached",
    27017: "MongoDB (Base NoSQL)",
    27018: "MongoDB (Shard)",

    # --- DevOps, CI/CD & Cloud ---
    2375: "Docker API (Clair - CRITIQUE ! Permet Root sur l'hôte)",
    2376: "Docker API (Sécurisé)",
    5000: "Docker Registry (Dépôt d'images privées)",
    6443: "Kubernetes API (Orchestration)",
    9000: "Portainer / SonarQube",
    9090: "Prometheus (Monitoring Cloud)",
    10250: "Kubernetes Kubelet API",

    # --- Découvertes Locales (Windows & Virtualisation) ---
    903: "VMware Console Display",
    913: "VMware Auth Daemon",
    4192: "Port Éphémère / Inconnu",
    5040: "CDPSvc (Connected Devices Platform - Windows Sync)",
    5800: "VNC HTTP Access (Interface Web d'administration)",
    5939: "TeamViewer IPC (Vulnérable LPE / Inter-Process)",
    7680: "WUDO (Windows Update Delivery Optimization - P2P local)"
}