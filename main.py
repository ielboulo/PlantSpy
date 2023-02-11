from fastapi import FastAPI, UploadFile, Depends
import io
import numpy as np
from PIL import Image
from Models import pred_categorie, pred_healthy, predict, preprocessing
from authenticate import authenticate_user, check_access


app = FastAPI(title = "PlantsPy Model",
              description = "Mettre en production un modèle de ML")

@app.get("/Healthcheck", 
         tags=["Statut"], 
         name="Permet de vérifier l'état de l'API")
async def get_health():
    return {"status": "OK"}


@app.post("/predict_categorie",
           tags=["Utilisateurs"], 
           name="Permet de connaître la catégorie de la plante")
async def predict_categorie(file: UploadFile,
                            user_validation: dict = Depends(authenticate_user)):
    
    image = Image.open(io.BytesIO(await file.read()))
    check_access(user_validation["access_level"], "user")
    image = preprocessing(image)
    prediction = pred_categorie(image)
   
    return {"prediction": prediction}


@app.post("/pred_healthy", 
          tags=["Utilisateurs"], 
          name="Permet de savoir si la plante est malade ou non")
async def predict_healthy(file: UploadFile,
                          user_validation: dict = Depends(authenticate_user)):
    
    image = Image.open(io.BytesIO(await file.read()))
    check_access(user_validation["access_level"], "user")
    image = preprocessing(image)
    prediction = pred_healthy(image)
   
    return {"prediction": prediction}


@app.post("/pred_TypeMaladie", 
          tags=["Utilisateurs"], 
          name="Permet de connaître la catégorie de la plante et le nom de la maladie si elle est connue")
async def predict_TypeMaladie(file: UploadFile,
                              user_validation: dict = Depends(authenticate_user)):
    
    image = Image.open(io.BytesIO(await file.read()))
    check_access(user_validation["access_level"], "user")
    image = preprocessing(image)
    prediction = predict(image)
    
    return {"prediction": prediction}
