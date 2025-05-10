# -*- coding: utf-8 -*-

from fastapi import APIRouter
from fastapi import status
from extensions.rest.rest import Rest

#from config.database.base.generic_model import GenericModel
#from sqlmodel import Field
#from sqlalchemy.ext.asyncio import AsyncSession
#from fastapi import Depends, Query
#from config.database.manager import db_manager, get_bd_session


#class User(GenericModel, table=True):
#    __tablename__ = 'users'
#    name: str = Field(index=True)


home_router = APIRouter()


#@home_router.get('')
#async def home_get(
#    session: AsyncSession = Depends(get_bd_session),
#    skip: int = 0,
#    limit: int = Query(default=100, le=200)
#):
#    users = await User.get_all(session, skip=skip, limit=limit, as_dict=True)
#    return Rest.response(
#        status_http=status.HTTP_200_OK,
#        message='OK',
#        data=users
#    )

@home_router.get('')
async def home_get():
    return Rest.response(
        status_http=status.HTTP_200_OK,
        message='OK',
        data={'Home': '🚀 ¡Bienvenid@ al ciberespacio! Listo para despegar ✨'}
    )


@home_router.post('')
async def home_post():
    return Rest.response(
        status_http=status.HTTP_200_OK,
        message='OK',
        data={'Home': '🚀 ¡Bienvenid@ al ciberespacio! Listo para despegar ✨'}
    )


@home_router.put('')
async def home_put():
    return Rest.response(
        status_http=status.HTTP_200_OK,
        message='OK',
        data={'Home': '🚀 ¡Bienvenid@ al ciberespacio! Listo para despegar ✨'}
    )


@home_router.delete('')
async def home_delete():
    return Rest.response(
        status_http=status.HTTP_200_OK,
        message='OK',
        data={'Home': '🚀 ¡Bienvenid@ al ciberespacio! Listo para despegar ✨'}
    )

