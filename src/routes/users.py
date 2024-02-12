from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
import sys

sys.path.append(str(BASE_DIR))

from fastapi import APIRouter, Depends, status, UploadFile, File
from sqlalchemy.orm import Session


from src.database.db import get_db
from src.database.models import User
from src.repository import users as repository_users
from src.services.auth import auth_service
from src.conf.config import settings
from src.schemas import UserResponse
from src.services.cloud_image import CloudImage

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me/", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(auth_service.get_current_user)):
    """
    Get information about the current user

    :param current_user: Current user obtained via Depends
    :return: The response user object
    """
    return current_user


@router.patch('/avatar', response_model=UserResponse)
async def update_avatar_user(file: UploadFile = File(), current_user: User = Depends(auth_service.get_current_user),
                             db: Session = Depends(get_db)):
    """
    Update user avatar

    :param file: Uploaded image (avatar) file
    :param current_user: Current user obtained via Depends
    :param db: The SQLAlchemy session object
    :return: The response user object
    """
    public_id = CloudImage.generate_name_avatar(current_user.email)
    r = CloudImage.upload(file.file, public_id)
    src_url = CloudImage.get_url_for_avatar(public_id, r)
    user = await repository_users.update_avatar(current_user.email, src_url, db)
    return user