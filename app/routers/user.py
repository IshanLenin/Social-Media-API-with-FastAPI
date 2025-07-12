from .. import models, schemas, utils
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from ..database import get_db

router=APIRouter( # Create a new API router instance
    prefix="/users",
    tags=['Users'] # Prefix for all routes in this router
) 

# Create a new user
# This endpoint allows the creation of a new user with a hashed password
from sqlalchemy.exc import IntegrityError

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user_dict = user.model_dump()
    user_dict["password"] = hashed_password

    new_user = models.User(**user_dict)
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError as e:
        db.rollback()  # Always rollback on DB errors
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists."
        )


@router.get("/{id}", response_model=schemas.UserOut)  # Get a specific user by id
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()  # Query the user by id from the database
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"User with id {id} was not found")
    return user