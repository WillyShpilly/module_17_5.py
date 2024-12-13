from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated
from app.models import User, Task
from app.schemas import CreateUser, UpdateUser
from sqlalchemy import insert, select, update, delete
from slugify import slugify

router = APIRouter(prefix='/user', tags=['user'])


@router.get('/')
async def all_user(db: Annotated[Session, Depends(get_db)]):
    users = db.scalars(select(User)).all()
    return users


@router.get('/user_id/{user_id}')
async def user_by_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    users = db.scalar(select(User).where(User.id == user_id))
    if users is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found'
        )

    return users


@router.post('/create')
async def create_user(user: CreateUser, db: Annotated[Session, Depends(get_db)]):
    db.execute(insert(User).values(username=user.username,
                                   firstname=user.firstname,
                                   lastname=user.lastname,
                                   age=user.age,
                                   slug=slugify(user.username)))

    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }


@router.put('/update')
async def update_user(db: Annotated[Session, Depends(get_db)], user_id: int, update_user: UpdateUser):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found'
        )
    db.execute(update(User).where(User.id == user_id).values(
        firstname=update_user.firstname,
        slug=slugify(update_user.firstname),
        lastname=update_user.lastname,
        age=update_user.age,
        ))

    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'User update is successful'
    }


@router.delete('/delete')
async def delete_user(db: Annotated[Session, Depends(get_db)], user_id: int):
    user = db.scalar(select(User).where(User.id == user_id))
    if user:
        db.execute(delete(Task).where(Task.user_id == user_id))
        db.execute(delete(User).where(User.id == user_id))
        db.commit()
        return {
            'status_code': status.HTTP_200_OK,
            'transaction': 'User delete is successful'}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='User was not found'
    )