from jose import JWTError, jwt
from datetime import datetime, timedelta
from modules import schemas
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

#Purpose : Manage jwt access token



oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


SECRET_KEY = "48646546468464s65fesfqs5ef45ef45e4fefef45zdazdsa4sd4zd8e484ht84htfyjndrfg4qsefdaqf"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

#Function to create the access token
def create_access_token(data: dict):
    to_encode = data.copy()
    
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

#Function to verify the access token 
def verify_access_token(token: str, credentials_exception):
    
    try :
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        id: str = payload.get("user_id")
        
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    
    return token_data

# Extract the id from the token

def get_current_user (token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    
    return verify_access_token(token, credentials_exception)