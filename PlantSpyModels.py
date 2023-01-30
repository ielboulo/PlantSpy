
import streamlit as st
import inspect
import textwrap
import time
import numpy as np
from utils import show_code

import streamlit as st
import pandas as pd
from keras.preprocessing.image import load_img
from tempfile import NamedTemporaryFile
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import cv2
import tensorflow as tf
import os
import pathlib
from PIL import Image
import seaborn as sns
import plotly.express as px
from sklearn.model_selection import train_test_split
import random
# %matplotlib inline

from matplotlib import cm
from imblearn.under_sampling import RandomUnderSampler

from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import GlobalAveragePooling2D
from tensorflow.keras.utils import to_categorical
from keras.preprocessing.image import ImageDataGenerator

from tensorflow.keras import Sequential
from tensorflow.keras import callbacks

from tensorflow.keras.applications.vgg16 import VGG16

from sklearn import metrics  # Pour évaluer les modèles



# Plant Spy AI Deep Learning Models :

model_categorie = tf.keras.models.load_model('./Models/model_LeNet1_Categorie_AllData_Softmax')
model_healthy = tf.keras.models.load_model("./Models/model_isHealthy_18K")
model_maladieTomato = tf.keras.models.load_model('./Models/model_Tomate_avecHealthy_softmax')
model_maladiePotato = tf.keras.models.load_model('./Models/model_Potato1_avecHealthy')
model_maladieCorn   = tf.keras.models.load_model('./Models/model_Corn_Healthy')
model_maladieApple  = tf.keras.models.load_model('./Models/model_Apple_Healthy')
model_maladieGrape  = tf.keras.models.load_model('./Models/model_Grape1_Healthy')

########################################################################################


dict_categorie = {0: 'Apple', 1: 'Blueberry', 2: 'Cherry', 3: 'Corn', 4: 'Grape', 5: 'Orange', 6: 'Peach',
                  7: 'Pepper', 8: 'Potato', 9: 'Raspberry', 10: 'Soybean', 11: 'Squash', 12: 'Strawberry', 13: 'Tomato'}

# Grape
dict_maladie_Grape1 = {0: 'Black_rot',
                       1: 'Esca_(Black_Measles)',
                       2: 'Leaf_blight_(Isariopsis_Leaf_Spot)',
                       3: 'healthy'}

# POTATO

dict_maladie_Potato1 = {0: 'Early_blight',
                        1: 'Late_blight',
                        2: 'healthy'}

# TOMATO

dict_maladie_Tomato1 = {0: 'Bacterial_spot',
                        1: 'Early_blight',
                        2: 'Late_blight',
                        3: 'Leaf_Mold',
                        4: 'Septoria_leaf_spot',
                        5: 'Spider_mites Two-spotted_spider_mite',
                        6: 'Target_Spot',
                        7: 'Tomato_Yellow_Leaf_Curl_Virus',
                        8: 'Tomato_mosaic_virus',
                        9: 'healthy'}

# APPLE

dict_maladie_Apple1 = {0: 'Apple_scab',
                       1: 'Black_rot',
                       2: 'Cedar_apple_rust',
                       3: 'healthy'}

# CORN

dict_maladie_Corn1 = {2: 'Northern_Leaf_Blight',
                      1: 'Common_rust_',
                      0: 'Cercospora_leaf_spot Gray_leaf_spot',
                      3: 'healthy'}


########################################################################################

def pred_categorie(X):
    predict_categorie = model_categorie.predict(X)
    predict_categorie_class = predict_categorie.argmax(axis=1)
    prediction = (pd.DataFrame(predict_categorie_class, columns=['categorie'])).replace({"categorie": dict_categorie})
    prediction['confiance_categorie'] = predict_categorie.max(axis=1)
    return prediction


def pred_TypeMaladie(X, modele, dictionnaire):
    predict_maladie = modele.predict(X)
    predict_typeMaladie_class = predict_maladie.argmax(axis=1)
    prediction = (pd.DataFrame(predict_typeMaladie_class, columns=['maladie_pred'])).replace(
        {"maladie_pred": dictionnaire})
    prediction['confiance'] = predict_maladie.max(axis=1)
    return prediction


def pred_healthy(X):
    pred_healthy = model_healthy.predict(X)
    prediction = pd.DataFrame(pred_healthy.round(), columns=['maladie_pred']).astype('int')
    prediction['confiance'] = pred_healthy.max(axis=1) * prediction['maladie_pred'] + (
            1 - prediction['maladie_pred']) * (1 - pred_healthy.max(axis=1))
    prediction['maladie_pred'] = prediction['maladie_pred'].replace(to_replace=[0, 1], value=['Sick', 'Healthy'])
    return prediction


def predict(X):
    pred1 = pred_categorie(X)
    if pred1['categorie'][0] == "Tomato":
        pred2 = pred_TypeMaladie(X, model_maladieTomato, dict_maladie_Tomato1)
    elif pred1['categorie'][0] == "Potato":
        pred2 = pred_TypeMaladie(X, model_maladiePotato, dict_maladie_Potato1)
    elif pred1['categorie'][0] == "Apple":
        pred2 = pred_TypeMaladie(X, model_maladieApple, dict_maladie_Apple1)
    elif pred1['categorie'][0] == "Grape":
        pred2 = pred_TypeMaladie(X, model_maladieGrape, dict_maladie_Grape1)
    elif pred1['categorie'][0] == "Corn":
        pred2 = pred_TypeMaladie(X, model_maladieCorn, dict_maladie_Corn1)
    else:
        pred2 = pred_healthy(X)

    pred = pd.concat([pred1, pred2], axis=1)
    return pred


def predict_df(X):
    res = []
    for i in range(0, len(X)):
        res.append(predict(X.iloc[i, 0]))

    ########################################################################################


    ########################################################################################
    # afficher "level" nombres d'images : /Users/ilham_elbouloumi/PycharmProjects/pythonProject1/NewPlantDiseasesDataset/test/test
test_images = [
    './Models/NewPlantDiseasesDataset/test/test/AppleCedarRust1.JPG',
    './Models/NewPlantDiseasesDataset/test/test/AppleCedarRust4.JPG',
    './Models/NewPlantDiseasesDataset/test/test/AppleScab1.JPG',
    './Models/NewPlantDiseasesDataset/test/test/AppleScab3.JPG',
    './Models/NewPlantDiseasesDataset/test/test/CornCommonRust1.JPG',
    './Models/NewPlantDiseasesDataset/test/test/CornCommonRust2.JPG',
    './Models/NewPlantDiseasesDataset/test/test/CornCommonRust3.JPG',
    './Models/NewPlantDiseasesDataset/test/test/PotatoEarlyBlight1.JPG',
    './Models/NewPlantDiseasesDataset/test/test/PotatoEarlyBlight4.JPG',
    './Models/NewPlantDiseasesDataset/test/test/PotatoHealthy1.JPG',
    './Models/NewPlantDiseasesDataset/test/test/PotatoHealthy2.JPG',
    './Models/NewPlantDiseasesDataset/test/test/TomatoEarlyBlight1.JPG',
    './Models/NewPlantDiseasesDataset/test/test/TomatoHealthy1.JPG',
    './Models/NewPlantDiseasesDataset/test/test/TomatoYellowCurlVirus1.JPG',
    './Models/NewPlantDiseasesDataset/test/test/TomatoHealthy4.JPG'
]
list_names = ["Apple-CedarRust", "Apple-CedarRust", "Apple-Scab", "Apple-Scab", "Corn-CommonRust",
              "Corn-CommonRust ", "Corn-CommonRust",
              "Potato- EarlyBlight", "Potato- EarlyBlight", "Potato - Healthy", "Potato - Healthy",
              "Tomato - EarlyBlight",
              "Tomato Healthy", "Tomato -YellowCurlVirus ", "Tomato - Healthy"]
    ########################################################################################
