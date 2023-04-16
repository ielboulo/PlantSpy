from fastapi import FastAPI, HTTPException, Header, Depends,UploadFile, File,Request
from pydantic import BaseModel
import PlantSpyModels as plant
import jwt
import io
from PIL import Image
import pymongo
import uvicorn
from authenticate import *
from authorisation import *
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.api_key import APIKeyHeader
from starlette.status import HTTP_401_UNAUTHORIZED
from datetime import datetime, timedelta
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from werkzeug.utils import secure_filename
import os


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

# configure CORS

origins = [
    "http://plantspy.dev-boris.fr",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


# Configuration de la connexion à MongoDB
client = pymongo.MongoClient("mongodb://mongo:27017/")
db = client["plantspy"]

collection = db["utilisateurs"]

collection.insert_one({
    "username": "johndoe",
    "password": pwd_context.hash('secret'),
    "roles": ["admin", "categorie","sante","maladie"]
})
collection.insert_one({
    "username": "alice",
    "password": pwd_context.hash('wonderland'),
    "roles": ["categorie","sante","maladie"]
})

collection.insert_one({
    "username": "laboratoire",
    "password": pwd_context.hash('analyse'),
    "roles": ["stockage"]
})

collection.insert_one({
    "username": "bob",
    "password": pwd_context.hash('ordinateur'),
    "roles": ["categorie"]
})



async def verify_token(token: str = Depends(oauth2_scheme)):
    print("verification token")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            print('attention user vaut none')
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Vérifier si l'utilisateur est dans la base de données ou non
    user_db = collection.find_one({"username":username})
    user = get_user(user_db, username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Si tout est ok, renvoyer l'utilisateur
    print('VT user vaut:',user)
    print('VT userdb vaut:',user_db)
    print('VT user[\'roles\'] vaut:',user['roles'])
    return user


@app.post("/token", response_model=Token, tags=["Login via Oauth2"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user_db = collection.find_one({"username":form_data.username})
    print('collection', collection.find({}))
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

async def prediction_plante(url: str, token: str = Depends(verify_token)):
    """ A partir de l'URL on prédit le type de plante
    """
    if not has_role(token,'categorie'):
        raise HTTPException(status_code=403, detail="Rôle insuffisant")
    reponse = plant.pred_categorie(url)
    return reponse

# Route pour la prédiction du type de plante via url
@app.post("/prediction_plante_file",
           tags=['Prediction type de Plantes via un fichier'], 
           name="Permet de connaître la catégorie de la plante")
async def predict_categorie(file: UploadFile, token: str = Depends(verify_token)):
    
    image = Image.open(io.BytesIO(await file.read()))
    if not has_role(token,'categorie'):
        raise HTTPException(status_code=403, detail="Rôle insuffisant")
    image = plant.preprocessing(image)
    prediction = plant.pred_categorie_file(image)
   
    return {"prediction": prediction}

# Route pour la prédiction de la santé de la plante via une url
@app.get("/prediction_sante_url", tags=['Prediction Santé de la Plante via url'])
async def prediction_sante(url: str, token: str = Depends(verify_token)):
    print('le retour du token vaut : ',token)
    print('has role',has_role(token,'sante'))
    if not has_role(token,'sante'):
        raise HTTPException(status_code=403, detail="Rôle insuffisant")
    reponse = plant.pred_healthy(url)
    return reponse

# Route pour la prédiction de la santé de la plante via un fichier
@app.post("/prediction_sante_file", tags=["Prediction Santé de la Plante via un fichier"], name="Permet de savoir si la plante est malade ou non")
async def predict_healthy(file: UploadFile, token: str = Depends(verify_token)):
    
    image = Image.open(io.BytesIO(await file.read()))
    if not has_role(token,'sante'):
        raise HTTPException(status_code=403, detail="Rôle insuffisant")
    image = plant.preprocessing(image)
    prediction = plant.pred_healthy_file(image)
   
    return {"prediction": prediction}

# Route pour la prédiction de la maladie de la plante via une url
@app.get("/prediction_maladie_url", tags=['Prediction de la Maladie de la Plante via une url'])

async def prediction_maladie(url: str, token: str = Depends(verify_token)):
    """ A partir de l'URL on prédit le type de plante
    """
    if not has_role(token,'maladie'):
        raise HTTPException(status_code=403, detail="Rôle insuffisant")
    reponse = plant.predict(url)
    return reponse


# Route pour la prédiction de la maladie de la plante via une url
@app.post("/prediction_maladie_file", 
          tags=["Prediction de la Maladie de la Plante via un fichier"], 
          name="Permet de connaître la catégorie de la plante et le nom de la maladie si elle est connue")
async def predict_TypeMaladie(file: UploadFile, token: str = Depends(verify_token)):
    
    image = Image.open(io.BytesIO(await file.read()))
    if not has_role(token,'maladie'):
        raise HTTPException(status_code=403, detail="Rôle insuffisant")
    image = plant.preprocessing(image)
    prediction = plant.predict_file(image)
    
    return {"prediction": prediction}

#ajout image
@app.post('/ajout_maladie', tags=["Ajout de photo maladie dans le dossier pour entrainement "])
async def ajout_maladie(request: Request):
    form_data = await request.form()
    print(form_data)
    if form_data['file'].filename == '':
        return JSONResponse({'error': 'No image uploaded'}, status_code=400)
    categorie_plante = form_data['categorie_plante']
    sante_plante = form_data['sante_plante']
    maladie_plante = form_data['maladie_plante']
    filename = secure_filename(f"{categorie_plante}_{sante_plante}_{maladie_plante}.jpg")
    file_path = os.path.join('images', filename)

    with open(file_path, 'wb') as f:
        f.write(await form_data['file'].read())
        print('fichier',f,' recorded')
    
    with open('images/logs.txt', 'a') as file:
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        file.write("Positif\n")
        print('logs updated')
        
    return JSONResponse({'success': 'Image uploaded successfully'}, status_code=200)


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)