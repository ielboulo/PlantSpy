import subprocess
import os
import json
import pandas as pd
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.models import Variable

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

API_BASE_URL = 'http://localhost:8000' #adresse de l'API

def test_api_with_images():
    image_directory = os.path.join(os.path.dirname(__file__), 'Images')
    image_files = [f for f in os.listdir(image_directory) if f.endswith('.JPG')]

    json_list = []

    for image_file in image_files:
        image_path = os.path.join(image_directory, image_file)

        curl_command = f"curl -X POST {API_BASE_URL}/prediction_maladie_file -H 'accept: application/json' -H 'Content-Type: multipart/form-data' -F 'file=@{image_path};type=image/jpeg'"
        response = subprocess.run(curl_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, universal_newlines=True)

        if response.returncode == 0:
            plant_disease_json = json.loads(response.stdout)
        else:
            print(f"Error executing cURL command for {image_file}: {response.stderr}")
            continue

        if 'prediction' in plant_disease_json:
            plant_disease = plant_disease_json['prediction']['maladie_pred']['0']
        else:
            plant_disease = 'Healthy'

        plant_type = plant_disease_json['prediction']['categorie']['0']
        confiance_plant_type = plant_disease_json['prediction']['confiance_categorie']['0']
        plant_health = plant_disease_json['prediction']['maladie_pred']['0']
        confiance_health = plant_disease_json['prediction']['confiance']['0']

        json_list.append({
            'file': image_file,
            'confiance_plant_health': confiance_plant_type,
            'plant_type': plant_type,
            'plant_health': plant_health,
            'confiance_health': confiance_health,
            'plant_disease': plant_disease,
        })

    json_path = '/results/json/' + datetime.now().strftime("%Y-%m-%d_%H:%M") + '.json'

    if not os.path.exists(os.path.dirname(json_path)):
        os.makedirs(os.path.dirname(json_path))

    with open(json_path, 'w') as json_file:
        json.dump(json_list, json_file)

    return json_list


def transform_data_into_csv(json_data, filename='results.csv'):
    df = pd.DataFrame(json_data)
    csv_path = '/results/csv/' + filename

    if not os.path.exists(os.path.dirname(csv_path)):
        os.makedirs(os.path.dirname(csv_path))

    df.to_csv(csv_path, index=False)

dag = DAG(
'test_api_dag',
default_args=default_args,
description='Test API with Images',
schedule_interval=timedelta(days=1),
start_date=datetime(2023, 3, 28),
catchup=False,
)

test_api_task = PythonOperator(
task_id='test_api_with_images',
python_callable=test_api_with_images,
dag=dag,
)

transform_data_task = PythonOperator(
task_id='transform_data_into_csv',
python_callable=transform_data_into_csv,
op_args=[test_api_task.output],
dag=dag,
)

test_api_task >> transform_data_task
