#il faut d'abord installer airflow:

mkdir ./dags ./logs ./plugins

echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env

docker-compose up airflow-init

#placer le fichier test_api_dag.py et le dossier Images dans le dossier ./dag
mv Image ./dags
cp test_api_dag.py ./dags

#lancer le service airflow
docker-compose up -d
