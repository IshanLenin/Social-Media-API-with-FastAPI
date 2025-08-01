from fastapi import APIRouter, Depends, HTTPException, status,Response
from sqlalchemy.orm import Session
from .. import database, schemas, models,utils,oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


router=APIRouter(

    tags=['Authentication']
)
 
@router.post('/login',response_model=schemas.Token)  # Login endpoint
# This endpoint allows users to log in and receive an access token

def login(user_credentials: OAuth2PasswordRequestForm= Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()  # Query user by email

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials"
        )

    # Compare entered password with hashed password in database
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials"
        )
    
    access_token = oauth2.create_access_token(data={"user_id":user.id})  # Create access token

    return {"access_token": access_token, "token_type": "bearer"}
