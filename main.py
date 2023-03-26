from fastapi import FastAPI, HTTPException, Header, Depends,UploadFile
from pydantic import BaseModel
import PlantSpyModels as plant
import jwt
import io
from PIL import Image
import pymongo
import uvicorn
from authenticate import *
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.api_key import APIKeyHeader
from starlette.status import HTTP_401_UNAUTHORIZED
from datetime import datetime, timedelta

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


# Configuration de la connexion à MongoDB
client = pymongo.MongoClient("mongodb://mongo:27017/")
db = client["plantspy"]

collection = db["utilisateurs"]

collection.insert_one({
    "username": "johndoe",
    "password": pwd_context.hash('secret')
})
collection.insert_one({
    "username": "alice",
    "password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"
})

# Définition des modèles pour les entrées et les sorties
class User(BaseModel):
    username: str
    password: str



# @app.post("/token")
# async def login(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = authenticate_user(form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")
#     access_token = create_access_token(data={"sub": user})
#     return {"access_token": access_token}

# @app.get("/secret")
# def read_secret_data(    current_user: User = Depends(OAuth2PasswordBearer(tokenUrl="/token"))):
#     return {"message": "Welcome to the secret data"}


# def validate_token(token: str):
#     try:
#         decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         return decoded
#     except (jwt.exceptions.InvalidTokenError, jwt.exceptions.DecodeError):
#         raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Not authorized")


# to get a string like this run:
# openssl rand -hex 32



@app.post("/token", response_model=Token, tags=["Login via Oauth2"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user_db = collection.find_one({"username":form_data.username})
    print('requete user',user_db)
    user = authenticate_user(user_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user['username']}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# Route pour verifier le statut de l'API
@app.get("/Healthcheck", 
         tags=["Statut"], 
         name="Permet de vérifier l'état de l'API")
async def get_health():
    return {"status": "OK"}

# Route pour la prédiction du type de plante via url
@app.get("/prediction_plante_url", tags=['Prediction type de Plantes via url'])

async def prediction_plante(url: str):
    """ A partir de l'URL on prédit le type de plante
    """
    reponse = plant.pred_categorie(url)
    return reponse

# Route pour la prédiction du type de plante via url
@app.post("/prediction_plante_file",
           tags=['Prediction type de Plantes via un fichier'], 
           name="Permet de connaître la catégorie de la plante")
async def predict_categorie(file: UploadFile):
    
    image = Image.open(io.BytesIO(await file.read()))
    #check_access(user_validation["access_level"], "user")
    image = plant.preprocessing(image)
    prediction = plant.pred_categorie_file(image)
   
    return {"prediction": prediction}

# Route pour la prédiction de la santé de la plante via une url
@app.get("/prediction_sante_url", tags=['Prediction Santé de la Plante via url'])
async def prediction_sante(url: str, token: str = Depends(oauth2_scheme)):
    reponse = plant.pred_healthy(url)
    return reponse

# Route pour la prédiction de la santé de la plante via un fichier
@app.post("prediction_sante_file", tags=["Prediction Santé de la Plante via un fichier"], name="Permet de savoir si la plante est malade ou non")
async def predict_healthy(file: UploadFile):
    
    image = Image.open(io.BytesIO(await file.read()))
    #check_access(user_validation["access_level"], "user")
    image = plant.preprocessing(image)
    prediction = plant.pred_healthy_file(image)
   
    return {"prediction": prediction}

# Route pour la prédiction de la maladie de la plante via une url
@app.get("/prediction_maladie_url", tags=['Prediction de la Maladie de la Plante via une url'])

async def prediction_maladie(url: str):
    """ A partir de l'URL on prédit le type de plante
    """
    reponse = plant.predict(url)
    return reponse


# Route pour la prédiction de la maladie de la plante via une url
@app.post("/prediction_maladie_file", 
          tags=["Prediction de la Maladie de la Plante via un fichier"], 
          name="Permet de connaître la catégorie de la plante et le nom de la maladie si elle est connue")
async def predict_TypeMaladie(file: UploadFile):
    
    image = Image.open(io.BytesIO(await file.read()))
    #check_access(user_validation["access_level"], "user")
    image = plant.preprocessing(image)
    prediction = plant.predict_file(image)
    
    return {"prediction": prediction}

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)