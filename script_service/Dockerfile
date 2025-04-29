# script_service/Dockerfile

# Utilisation d'une version slim suffisante pour le projet
FROM python:3.11-slim

WORKDIR /app

# Copie les fichiers de script
COPY . /app

# Installe les dépendances nécessaires
RUN pip install pandas requests

# Commande par défaut
CMD ["python", "main.py"]