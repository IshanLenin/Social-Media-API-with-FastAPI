from .. import models, schemas,oauth2
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List, Optional
from sqlalchemy import func

router=APIRouter( # Create a new API router instance
    prefix="/posts",
    tags=['Posts'] # Prefix for all routes in this router
)  

@router.get("/sqlalchemy") #Decorator to define the function as a GET endpoint
def test_posts(db: Session = Depends(get_db)): # Dependency to get a database session

    posts= db.query(models.Post).all()  # Query all posts from the database
    return posts


@router.get("/", response_model=List[schemas.PostOut]) # Get all posts with pagination and search functionality
def get_posts(db: Session = Depends(get_db),
              user_id: int = Depends(oauth2.get_current_user), # Get the current user
              limit: int = 10, # Limit the number of posts returned
              skip: int = 0, # Skip the first 'skip' number of posts
              search: Optional[str] = ""):  # Search for posts by title
    
   
    results = ( 
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True)
        .filter(models.Post.title.contains(search))
        .group_by(models.Post.id)
        .limit(limit) 
        .offset(skip)
        .all() # Get posts with votes count
    )

    return results

@router.post("/", status_code=status.HTTP_201_CREATED, 
             response_model=schemas.Post) # Create a new post
def create_posts(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: models.User= Depends(oauth2.get_current_user)
):  # Create a new post with the current user's ID 
    
    new_post = models.Post(owner_id=current_user.id,
                           **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post # Return the newly created post


@router.get("/{id}", response_model=schemas.PostOut) # Get a specific post by id
def get_post(id: int,response: Response, 
             db: Session = Depends(get_db),
             current_user:int=Depends(oauth2.get_current_user)):
     # Get a specific post by id
    
    test_post= (db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True)).filter(models.Post.id == id).group_by(models.Post.id).first()  # Query the post by id from the database
    
    # If the post does not exist, return a 404 error
    if not test_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {id} was not found")
    return test_post if test_post else {"error": "Post not found"}


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: models.User= Depends(oauth2.get_current_user)):
   # Delete a specific post by id
   
   query= db.query(models.Post).filter(models.Post.id == id)  # Query the post by id from the database
   
   post =query.first()  # Get the first post that matches the query
  
   if post is None: # If the post does not exist, return a 404 error
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                           detail=f"Post with id {id} was not found") 
   
   if getattr(post, "owner_id", None) != current_user.id:  # Check if the current user is the owner of the post
       raise HTTPException(
           status_code=status.HTTP_403_FORBIDDEN,
           detail="Not authorized to perform requested action"
       )
   
   query.delete(synchronize_session=False) # Delete the post from the database
   db.commit()
   return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schemas.Post) # Update a specific post by id
def update_post(id: int, post_data: schemas.PostCreate, db: Session = Depends(get_db),current_user:models.User=Depends(oauth2.get_current_user)):
    # Update a specific post by id

    query = db.query(models.Post).filter(models.Post.id == id)
    post = query.first()

    
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with id {id} was not found"
        )
    
    if getattr(post, "owner_id", None) != current_user.id: # Check if the current user is the owner of the post
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action"
        )

    query.update(post_data.model_dump(), synchronize_session=False)  # type: ignore[arg-type]
    db.commit()
    
    return query.first()