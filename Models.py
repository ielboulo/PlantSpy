import pandas as pd
import numpy as np
from Dictionnaire import model_categorie, model_healthy, model_maladieTomato, model_maladiePotato, model_maladieCorn, model_maladieGrape, model_maladieApple, dict_categorie, dict_maladie_Grape1, dict_maladie_Corn1, dict_maladie_Apple1, dict_maladie_Potato1, dict_maladie_Tomato1


def pred_categorie(X):
    predict_categorie = model_categorie.predict(X)
    predict_categorie_class = predict_categorie.argmax(axis=1)
    prediction = (pd.DataFrame(predict_categorie_class, columns=['categorie'])).replace({"categorie": dict_categorie})
    prediction['confiance_categorie'] = predict_categorie.max(axis=1)
    return prediction.to_dict()

def pred_healthy(X):
    pred_healthy = model_healthy.predict(X)
    prediction = pd.DataFrame(pred_healthy.round(), columns=['maladie_pred']).astype('int')
    prediction['confiance'] = pred_healthy.max(axis=1) * prediction['maladie_pred'] + (
            1 - prediction['maladie_pred']) * (1 - pred_healthy.max(axis=1))
    prediction['maladie_pred'] = prediction['maladie_pred'].replace(to_replace=[0, 1], value=['Sick', 'Healthy'])
    return prediction.to_dict()

def pred_TypeMaladie(X, modele, dictionnaire):
    predict_maladie = modele.predict(X)
    predict_typeMaladie_class = predict_maladie.argmax(axis=1)
    prediction = (pd.DataFrame(predict_typeMaladie_class, columns=['maladie_pred'])).replace(
        {"maladie_pred": dictionnaire})
    prediction['confiance'] = predict_maladie.max(axis=1)
    return prediction.to_dict()

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

    prediction = pd.concat([pd.DataFrame(pred1), pd.DataFrame(pred2)], axis=1)
    return prediction.to_dict()

def preprocessing(image):
    image = image.resize((100, 100))
    image = np.array(image)
    image = image / 255.0
    image = np.expand_dims(image, axis=0)
    return image