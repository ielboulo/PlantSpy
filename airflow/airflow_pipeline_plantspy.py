import os
import numpy as np
from PIL import Image
import tensorflow as tf
from datetime import datetime
import pandas as pd
import re
from airflow import DAG 
from airflow.operators.python_operator import PythonOperator


dict_categorie = {0: 'Apple', 1: 'Blueberry', 2: 'Cherry', 3: 'Corn', 4: 'Grape', 5: 'Orange', 6: 'Peach',
                  7: 'Pepper', 8: 'Potato', 9: 'Raspberry', 10: 'Soybean', 11: 'Squash', 12: 'Strawberry', 13: 'Tomato'}


def preprocessing(image):
    image = image.resize((100,100))
    image = np.array(image)
    image = image / 255.0
    # image = np.expand_dims(image, axis=0)
    return image.tolist()


def load_model():
    model_path = "/app/models"
    model = tf.keras.models.load_model(model_path)
    model_json = model.to_json()
    return model_json


def load_images(image_folder):
    images = []
    for filename in os.listdir(image_folder):
        if filename.endswith('.JPG') or filename.endswith('.jpg'):
            img = Image.open(os.path.join(image_folder, filename))
            img = preprocessing(img)
            images.append((filename, img))
    return images


def pred_categorie(X, model):
    filenames = [img[0] for img in X]  
    X = [img[1] for img in X]
    model_categorie = tf.keras.models.model_from_json(model)
    model_categorie.load_weights("/app/models/variables/variables")
    predict_categorie = model_categorie.predict(X)
    predict_categorie_class = predict_categorie.argmax(axis=1)
    prediction = (pd.DataFrame(predict_categorie_class, columns=['categorie'])).replace({"categorie": dict_categorie})
    prediction['confiance_categorie'] = predict_categorie.max(axis=1)
    prediction['filename'] = filenames 
    return prediction.to_dict()


def save_predictions_to_csv(predictions):
    results_dir = "/app/results"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    df = pd.DataFrame(predictions)
    df = df[['filename', 'categorie', 'confiance_categorie']]  
    csv_path = os.path.join(results_dir, 'predictions.csv')
    df.to_csv(csv_path, index=False)



default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2023, 4, 11),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0
}

dag = DAG(
    dag_id="image_prediction_pipeline",
    default_args=default_args,
    schedule_interval=None
)

load_model_task = PythonOperator(
    task_id="load_model",
    python_callable=load_model,
    dag=dag
)

load_images_task = PythonOperator(
    task_id="load_images",
    python_callable=load_images,
    op_kwargs={"image_folder": "/app/Images"},
    dag=dag
)

predict_task = PythonOperator(
    task_id="predict_task",
    python_callable=pred_categorie,
    op_kwargs={"X": load_images_task.output, "model": load_model_task.output},
    dag=dag
)

save_predictions_task = PythonOperator(
    task_id="save_predictions",
    python_callable=save_predictions_to_csv,
    op_kwargs={"predictions": predict_task.output},
    dag=dag
)



load_model_task >> predict_task
load_images_task >> predict_task
predict_task >> save_predictions_task


