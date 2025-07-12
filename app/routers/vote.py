from fastapi import APIRouter, Depends, HTTPException, status
from .. import models, schemas, oauth2,database
from ..database import get_db
from sqlalchemy.orm import Session

router=APIRouter(
    prefix="/vote",
    tags=['Votes']
)

@router.post("/",status_code=status.HTTP_201_CREATED) # Create a new vote
# This endpoint allows users to vote on a post
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user:models.User = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.Post_id).first()  # Check if the post exists
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {vote.Post_id} does not exist")

    vote_query=db.query(models.Vote).filter(models.Vote.post_id == vote.Post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    
    if vote.dir == 1: # Upvote
        if found_vote: # If the user has already voted on this post
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                                detail="User has already voted on this post")
        new_vote = models.Vote(post_id=vote.Post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Vote added successfully"}
    
    else: # Downvote
        if not found_vote: # If the user is trying to downvote but has not voted before
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail="Vote does not exist")
        vote_query.delete(synchronize_session=False) # Delete the vote
        db.commit()
        return {"message": "Vote deleted successfully"}
