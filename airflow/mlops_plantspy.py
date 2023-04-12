import os
import numpy as np
from PIL import Image
import tensorflow as tf
from datetime import datetime
import pandas as pd
import re
from airflow import DAG 
from airflow.operators.python_operator import PythonOperator
from sklearn.preprocessing import LabelEncoder

from tensorflow.keras.layers import Input, Dense 
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dropout 
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Conv2D 
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import GlobalAveragePooling2D
from tensorflow.keras.utils import to_categorical
from keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam

from tensorflow.keras import Sequential
from tensorflow.keras import callbacks



dict_categorie = {0: 'Apple', 1: 'Blueberry', 2: 'Cherry', 3: 'Corn', 4: 'Grape', 5: 'Orange', 6: 'Peach',
                  7: 'Pepper', 8: 'Potato', 9: 'Raspberry', 10: 'Soybean', 11: 'Squash', 12: 'Strawberry', 13: 'Tomato'}


def extract_category_from_filename(filename):
    match = re.match(r"([A-Z][a-z]+)([A-Z][a-z]+)(.*)", filename)
    if match:
        category = match.group(1)
    else:
        category = "unknown"
    return category


def preprocessing(image):
    image = image.resize((100,100))
    image = np.array(image)
    image = image / 255.0
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
    df['true_category'] = df['filename'].apply(extract_category_from_filename)
    df = df[['filename', 'true_category', 'categorie', 'confiance_categorie']]  
    csv_path = os.path.join(results_dir, 'predictions.csv')
    df.to_csv(csv_path, index=False)

def calculate_accuracy(predictions):
    df = pd.DataFrame(predictions)
    df['true_category'] = df['filename'].apply(extract_category_from_filename)
    df['is_correct'] = df['true_category'] == df['categorie']
    accuracy = df['is_correct'].mean()
    
    accuracy_file_path = "/app/results/accuracy.txt"
    with open(accuracy_file_path, "w") as f:
        f.write(f"Model accuracy: {accuracy:.4f}")

    return accuracy

def load_images_ml(image_folder):
    X_train0=[]
    y_train0=[]
    y2_train0=[]
    print('début du traitement train')
    folder = image_folder+'train/'
    for path, dirs, files in os.walk(image_folder):
        for repertoire in dirs:
            chemin=image_folder+repertoire
            print('traitement train dans le chemin:', chemin)
            max = 50
            compteur = 0
            for images in os.listdir(chemin):
                if(compteur<max):
                    img = Image.open(os.path.join(chemin, images))
                    img_resized = preprocessing(img)
                    X_train0.append(np.array(img_resized))
                    y_train0.append(repertoire.split('___')[0])   # On recupere la categorie de plante
                    y2_train0.append(repertoire.split('___')[1]) # On recupere la maladie
                    compteur+=1

    X_train0 = np.array(X_train0)
    X_train0 = X_train0.astype('float32')  
    y_train0= np.array(y_train0)
    y2_train0= np.array(y2_train0) 
    print('y_train0 shape : ',y_train0.shape)
    print('y2_train0 shape : ',y2_train0.shape)
    print('shape X_train0 : ',X_train0.shape)
    print('fin du traitement train')

    print('début du traitement valid')
    X_valid0=[]
    y_valid0=[]
    y2_valid0=[]
    folder = image_folder+'valid/'
    for path, dirs, files in os.walk(image_folder):
        for repertoire in dirs:
            chemin=image_folder+repertoire
            print('traitement valid dans le chemin:', chemin)
            max = 50
            compteur = 0
            for images in os.listdir(chemin):
                if(compteur<max):
                    img = Image.open(os.path.join(chemin, images))
                    img_resized = preprocessing(img)
                    X_valid0.append(np.array(img_resized))
                    y_valid0.append(repertoire.split('___')[0])   # On recupere la categorie de plante
                    y2_valid0.append(repertoire.split('___')[1]) # On recupere la maladie
                    compteur+=1

    X_valid0 = np.array(X_valid0)
    X_valid0 = X_valid0.astype('float32')  
    y_valid0= np.array(y_valid0)
    y2_valid0= np.array(y2_valid0) 
    print('y_valid0 shape : ',y_valid0.shape)
    print('y2_valid0 shape : ',y2_valid0.shape)
    print('shape X_valid0 : ',X_valid0.shape)
    print('fin du traitement valid')

    X_train = X_train0 / 255
    X_valid = X_valid0 / 255

    encoder =  LabelEncoder()
    y_train = encoder.fit_transform(y_train0)
    y_valid = encoder.transform(y_valid0)

    print('Shape of X Train:', X_train.shape)
    print('Shape of y train:',y_train.shape)

    print('Shape of X valid:', X_valid.shape)
    print('Shape of y valid:',y_valid.shape)

    early_stopping = callbacks.EarlyStopping(monitor = 'val_loss',
                        patience = 8,
                        mode = 'min',
                        restore_best_weights = True)

    lr_plateau = callbacks.ReduceLROnPlateau(monitor = 'val_loss',
                                patience=4,
                                factor=0.5,
                                verbose=2,
                                mode='min')
    
    train_data_generator = ImageDataGenerator(
            rotation_range=50,
            width_shift_range=1,
            height_shift_range=1,
            zoom_range=[0.7, 1.2],
            horizontal_flip=True)

    test_data_generator = ImageDataGenerator()
    batch_size = 25

    training_data = train_data_generator.flow(X_train, y_train, batch_size=batch_size)
    test_data = test_data_generator.flow(X_valid, y_valid, batch_size=batch_size)

    input_shape = (100,100,3)

    model_LeNet1 = Sequential()
    model_LeNet1.add(Conv2D(filters=30, kernel_size=(5, 5), padding='valid', input_shape=input_shape, activation='relu'))
    model_LeNet1.add(MaxPooling2D(pool_size=(3, 3)))
    model_LeNet1.add(Dropout(rate=0.2))
    model_LeNet1.add(Conv2D(filters=64, kernel_size=(3, 3), padding='valid', activation='relu'))
    model_LeNet1.add(MaxPooling2D(pool_size=(2, 2)))
    model_LeNet1.add(Conv2D(filters=32, kernel_size=(3, 3), padding='valid', activation='relu'))
    model_LeNet1.add(MaxPooling2D(pool_size=(2, 2)))
    model_LeNet1.add(Dropout(rate=0.2))
    model_LeNet1.add(Flatten())
    model_LeNet1.add(Dense(units=64, activation='relu'))
    model_LeNet1.add(Dense(units=14, activation='softmax')) #ML Essai softmax ala place de sigmoid

    model_LeNet1.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    model_LeNet1.summary()
    history_LeNet1 = model_LeNet1.fit_generator(generator = training_data, 
                              epochs = 10,
                              steps_per_epoch = len(X_train)//batch_size,
                              validation_data = test_data,
                              validation_steps = len(X_valid)//batch_size,
                              callbacks = [early_stopping,lr_plateau])
    tf.saved_model.save(model_LeNet1, "/app/models/periodique")



    return 17


default_args = {
    "owner": "airflow",
    "depends_on_past": True,
    "start_date": datetime(2023, 4, 11),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 3
}

dag = DAG(
    dag_id="test",
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
    op_kwargs={"image_folder": "/app/Images/test"},
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

calculate_accuracy_task = PythonOperator(
    task_id="calculate_accuracy",
    python_callable=calculate_accuracy,
    op_kwargs={"predictions": predict_task.output},
    dag=dag
)
periodic_training_task = PythonOperator(
    task_id="periodic_training",
    python_callable=load_images_ml,
    op_kwargs={"image_folder": "/app/Images/train/"},
    dag=dag
)


periodic_training_task >> [load_model_task , load_images_task] >> predict_task >> save_predictions_task >> calculate_accuracy_task





