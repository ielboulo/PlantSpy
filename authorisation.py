from typing import Union,List
from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None
    roles: List[str] = []

def has_role(user: User, role: str) -> bool:
    """
    Vérifie si l'utilisateur a le rôle spécifié.
    :param user: l'utilisateur
    :param role: le nom du rôle à vérifier
    :return: True si l'utilisateur a le rôle, False sinon
    """
    print('HR use : ',user)
    if not user['roles']:
        return False
    return role in user['roles']