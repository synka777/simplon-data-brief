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

## Structure des tables bassée sur les données en input:

#### Table `product`:
| Attribut | Type | Description |
| ------ | ------ | ------ |
| id | VARCHAR | Référence produit |
| name | TEXT | Nom du produit |
| price | DECIMAL | Prix du produit |
| qty | INTEGER | Stock initial |

#### Table `shop`:
| Attribut | Type | Description |
| ------ | ------ | ------ |
| id | INTEGER | ID du magasin |
| city | VARCHAR(255) | Ville |
| employees | INTEGER | Nombre de salariés |

#### Table `order`
| Attribut | Type | Description |
| ------ | ------ | ------ |
| date | TIMESTAMP | Date de la commande |
| product_id | VARCHAR | Réf. produit (foreign key) |
| qty | INTEGER | Quantité commandée |
| shop_id | INTEGER | ID magasin (foreign key) |