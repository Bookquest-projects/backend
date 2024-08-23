# Utilise une image de base Python 3.11
FROM python:3.11-slim

# Installer les dépendances système
RUN apt-get update && apt-get install -y libzbar0

# Définit le répertoire de travail dans le conteneur
WORKDIR /app

# Copie uniquement le fichier requirements.txt
COPY requirements.txt .

# Installe les dépendances du projet
RUN pip install --no-cache-dir -r requirements.txt

# Copie le reste des fichiers du projet dans le conteneur
COPY flaskProject_Pipeline/ .

# Expose le port 5000 (par défaut pour Flask)
EXPOSE 5000

# Commande pour lancer l'application
CMD ["python", "app/app.py"]