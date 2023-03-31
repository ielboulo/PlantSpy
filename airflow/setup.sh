#il faut d'abord installer airflow:
#avant de télécharger l'initialisation de airflow, changer le nom du fichier docker-compose déjà existant dans le dossier par docker-compose.yml
#et après le téléchargement et l'initialisation de airflow, penser a supprimer le docker-compose.yaml

wget https://dst-de.s3.eu-west-3.amazonaws.com/airflow_avance_fr/docker-compose/docker-compose.yaml

mkdir ./dags ./logs ./plugins

echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env

docker-compose up airflow-init

#placer le fichier test_api_dag.py et le dossier Images dans le dossier ./dag
mv Image ./dags
cp test_api_dag.py ./dags

#lancer le service airflow
docker-compose up -d
