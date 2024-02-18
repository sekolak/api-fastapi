from fastapi import Response, status, HTTPException, Depends, APIRouter
from modules import models, schemas
from sqlalchemy.orm import Session
from sqlalchemy import func
from modules.database import get_db
from typing import List, Optional
import oauth2

router = APIRouter(
    prefix="/posts",
    tags=['Users']
)

@router.get("/", response_model=List[schemas.PostOut])
#Here is query parameters
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limits: int = 10, skip: int = 0, search: Optional[str] = ""):

#    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limits).offset(skip).all()
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label
                      ("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, 
                                      isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limits).offset(skip).all()

    
    return posts

 
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    new_post = models.Post(owner_id=current_user.id, title=post.title, content=post.content, published=post.published)
    
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, response: Response, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    #post = db.query(models.Post).filter(models.Post.id == id).first()
    
    post = db.query(models.Post, func.count(models.Vote.post_id).label
                      ("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, 
                                      isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail=f"Not authorized to perform requested action")

    
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    print(current_user)
    
    post_querys = db.query(models.Post).filter(models.Post.id == id).first()
    
    post = post_querys.first()
    
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
        
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"Not authorized to perform requested action")
    
    post_querys.delete(synchronize_session=False)
    
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
 
@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    print(current_user)
    post_query = db.query(models.Post).filter(models.Post.id == id).first()
    post = post_query.first()

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"Not authorized to perform requested action")
        
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    
    post_query.update({'title': 'hey this is my updated title', 'content': 'this is my updated content'}, synchronize_session=False)

    db.commit()

    return {"data": post_query.first()}