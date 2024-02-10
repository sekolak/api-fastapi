from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from modules import models, schemas, utils
from sqlalchemy.orm import Session
from modules.database import get_db

router = APIRouter(
    prefix="/users"
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    #first create the hash of the password
    hashed_password = utils .hash(user.password)
    user.password = hashed_password

    #new_post = models.User(**vars(user))
    new_user = models.User(**user.model_dump())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user 

@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
   user =  db.query(models.User).filter(models.User.id == id).first()

   if not user:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                           detail=f"User with id: {id} does not exist")
   return user