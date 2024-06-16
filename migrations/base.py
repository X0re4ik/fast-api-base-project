from typing import List, Type

from src.models.base import Base
from src.models.user import RefreshToken, Secret, User

sqlalchemy_models: List[Type[Base]] = [
    User, 
    Secret, 
    RefreshToken
]