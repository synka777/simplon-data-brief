# simplon-data-brief

## Architecture du projet

Deux services:
- script_service: Exécute les scripts de manipulation/traitement data
- sqlite_service: Rend disponible les données en volume partagé

Communication:
- Pas besoin d'exposer de ports car sqlite n'est pas un serveur SQL à proprement parler; il suffira d'accéder au fichier .db mis à disposition en volume partagé
- Requêtes HTTP afin de récupérer les fichiers de données régulièrement

```bash
simplon-data-brief/
├── docker-compose.yml
├── script_service/
│   ├── Dockerfile
│   ├── main.py
│   ├── ...
│   └── ...
└── shared_data/ (=sqlite_service, volume monté)
```