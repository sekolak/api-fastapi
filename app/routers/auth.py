from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from modules import database, schemas, models, utils
import oauth2

#Purpose : create a secure jwt / 

router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    #check if the hashes matchs with the utils function defined into app/modules/utils
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    # Create a token with  the function using jwt into app/oauth2
    
    access_token = oauth2.create_access_token(data = {"user_id": user.id})
    
    #Return the token
    return {"acces_token": access_token, "token_type": "bearer"}