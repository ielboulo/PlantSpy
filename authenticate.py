from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.context import CryptContext


security = HTTPBasic()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

users = {"admin": {"username": "admin",
                   "hashed_password": pwd_context.hash('4dm1N'),
                   "access_level":"administrateur"},
         "alice" : {"username" :  "alice",
                    "hashed_password" : pwd_context.hash('wonderland'),
                    "access_level":"user"},
         "bob" : {"username" :  "bob",
                  "hashed_password" : pwd_context.hash('builder'),
                  "access_level":"user"},
         "clementine" : {"username" :  "clementine",
                         "hashed_password" : pwd_context.hash('mandarine'),
                         "access_level":"user"}
         }

def authenticate_user(credentials : HTTPBasicCredentials = Depends(security)):
    if (credentials.username not in users.keys()) or not(pwd_context.verify(credentials.password, users[credentials.username]['hashed_password'])):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiant ou mot de passe incorrecte",
            headers={"WWW-Authenticate": "Basic"})
    else:
        access_level = users[credentials.username]['access_level']
   
    return {"user_name":credentials.username,"access_level":access_level}

def check_access(user_access, access_requested):    
    if user_access != access_requested :
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès refusé")