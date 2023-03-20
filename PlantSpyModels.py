import pandas as pd
import tensorflow as tf
import cv2
import urllib
import numpy as np 
from urllib.request import urlopen, urlretrieve
from PIL import Image




# Plant Spy AI Deep Learning Models :

model_categorie = tf.keras.models.load_model(
    'models/model_LeNet1_Categorie_AllData_Softmax')


model_healthy = tf.keras.models.load_model("models/model_isHealthy_18K")

model_maladieTomato = tf.keras.models.load_model(
    'models/model_Tomate_avecHealthy_softmax')
model_maladiePotato = tf.keras.models.load_model(
    'models/model_Potato1_avecHealthy')
model_maladieCorn = tf.keras.models.load_model(
    'models/model_Corn_Healthy')
model_maladieApple = tf.keras.models.load_model(
    'models/model_Apple_Healthy')
model_maladieGrape = tf.keras.models.load_model(
    'models/model_Grape1_Healthy')

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
    X = img_process(X)
    print('Dans pred categorie avec X = ',X)
    predict_categorie = model_categorie.predict(X)
    print('predict_categorie',predict_categorie)
    predict_categorie_class = predict_categorie.argmax(axis=1)
    prediction = (pd.DataFrame(predict_categorie_class, columns=['categorie'])).replace({"categorie": dict_categorie})
    prediction['confiance_categorie'] = predict_categorie.max(axis=1)
    return prediction.to_dict()

def pred_categorie2(X):
    X = img_process(X)
    print('Dans pred categorie avec X = ',X)
    predict_categorie = model_categorie.predict(X)
    print('predict_categorie',predict_categorie)
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
    X = img_process(X)
    pred_healthy = model_healthy.predict(X)
    prediction = pd.DataFrame(pred_healthy.round(), columns=['maladie_pred']).astype('int')
    prediction['confiance'] = pred_healthy.max(axis=1) * prediction['maladie_pred'] + (
            1 - prediction['maladie_pred']) * (1 - pred_healthy.max(axis=1))
    prediction['maladie_pred'] = prediction['maladie_pred'].replace(to_replace=[0, 1], value=['Sick', 'Healthy'])
    return prediction


def predict(X):
    X = img_process(X)
    pred1 = pred_categorie2(X)
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
    return pred.to_dict()


def predict_df(X):
    res = []
    for i in range(0, len(X)):
        res.append(predict(X.iloc[i, 0]))

def preprocessing(image):
    image = image.resize((100, 100))
    image = np.array(image)
    image = image / 255.0
    image = np.expand_dims(image, axis=0)
    return image

def img_process(image):
    print('image = ',image)
    try:
        # resp = urlopen(image)
        # image = np.asarray(bytearray(resp.read()), dtype="uint8")
        im = 'test.jpg'
        fd = urllib.request.urlretrieve(image, im)
        image = Image.open(im) 
        image = image.convert('RGB')
        print('image 2  = ',image)
        # img = cv2.imread(image, cv2.IMREAD_COLOR)
        # img = np.asarray(Image.open('2007_000032.png'))
        # print(img)
        img_resized = image.resize((100, 100))
        print('img_resized = ',img_resized)
        image = np.array(img_resized)
        image = image / 255.0
        print('img shape = ',image.shape)
        image = np.expand_dims(image, axis=0)
        return image
        
    except Exception as e:
        print('Attention erreur exception : ----------',str(e))
        # return e
    return image
    ########################################################################################


    ########################################################################################
    # afficher "level" nombres d'images : models/NewPlantDiseasesDataset/test/test
test_images = [
    'models/NewPlantDiseasesDataset/test/test/AppleCedarRust1.JPG',
    'models/NewPlantDiseasesDataset/test/test/AppleCedarRust4.JPG',
    'models/NewPlantDiseasesDataset/test/test/AppleScab1.JPG',
    'models/NewPlantDiseasesDataset/test/test/AppleScab3.JPG',
    'models/NewPlantDiseasesDataset/test/test/CornCommonRust1.JPG',
    'models/NewPlantDiseasesDataset/test/test/CornCommonRust2.JPG',
    'models/NewPlantDiseasesDataset/test/test/CornCommonRust3.JPG',
    'models/NewPlantDiseasesDataset/test/test/PotatoEarlyBlight1.JPG',
    'models/NewPlantDiseasesDataset/test/test/PotatoEarlyBlight4.JPG',
    'models/NewPlantDiseasesDataset/test/test/PotatoHealthy1.JPG',
    'models/NewPlantDiseasesDataset/test/test/PotatoHealthy2.JPG',
    'models/NewPlantDiseasesDataset/test/test/TomatoEarlyBlight1.JPG',
    'models/NewPlantDiseasesDataset/test/test/TomatoHealthy1.JPG',
    'models/NewPlantDiseasesDataset/test/test/TomatoYellowCurlVirus1.JPG',
    'models/NewPlantDiseasesDataset/test/test/TomatoHealthy4.JPG'
]
list_names = ["Apple-CedarRust", "Apple-CedarRust", "Apple-Scab", "Apple-Scab", "Corn-CommonRust",
              "Corn-CommonRust ", "Corn-CommonRust",
              "Potato- EarlyBlight", "Potato- EarlyBlight", "Potato - Healthy", "Potato - Healthy",
              "Tomato - EarlyBlight",
              "Tomato Healthy", "Tomato -YellowCurlVirus ", "Tomato - Healthy"]
    ########################################################################################