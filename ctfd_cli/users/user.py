from ..config import *
from ..utils.logger import logger
from ..schemas import UserObject
from ..utils.handler import RequestHandler, Mode
from ..ctfd import CTFd

from typing import List, Dict
from pprint import pprint

class UserHandler:

    def __init__(self, ctfd : CTFd):
        self.ctfd = ctfd

    def __request__(self, req, default_ret_val=None, default_status_code = 200):
        if req.status_code != default_status_code:
            return default_ret_val
        try:
            data = req.json()['data']
        except KeyError:
            logger.error(f"An error occurred when parsing response: {req.json()}")
            return default_ret_val
        return data

    def get_all_users(self) -> List[UserObject]:

        '''
        NOTE: This function will NOT return users that have 'HIDDEN' attribute set.
            https://docs.ctfd.io/docs/api/redoc#tag/users/operation/get_user_list
        '''

        logger.info("Getting the list of all users...")
        r = RequestHandler.MakeRequest(
            mode=Mode.GET,
            url=f"{self.ctfd.ctfd_instance}/api/v1/users",
            token=self.ctfd.ctfd_token
        )

        data = self.__request__(r, [])
        if data == []:
            return []
        
        users = []
        for user in data:
            users.append(UserObject(**user))

        return users
    
    def get_user_by_id(self, id: int) -> UserObject|None:

        if id == None:
            return None

        logger.info(f"Getting info of user {id}")
        r = RequestHandler.MakeRequest(
            mode=Mode.GET,
            url=f"{self.ctfd.ctfd_instance}/api/v1/users/{id}",
            token=self.ctfd.ctfd_token
        )

        if r.status_code == 404:
            logger.error(f"User with id {id} doesn't exist.")
            return None

        data = self.__request__(r, None, 200)

        if data == None:
            return None
        
        return UserObject(**data)

    def get_user_by_name(self, name : str) -> UserObject|None:

        '''
        NOTE: This function will NOT return the user if they have 'HIDDEN' attribute set.
        '''

        logger.info(f"Getting info of user {name}")
        r = RequestHandler.MakeRequest(
            mode=Mode.GET,
            url=f"{self.ctfd.ctfd_instance}/api/v1/users",
            token=self.ctfd.ctfd_token
        )

        data = self.__request__(r, None, 200)
        if data == None:
            return None
        
        for user in data:
            if user['name'] == name:
                logger.info(f"User {name} has the ID {user['id']}")
                return self.get_user_by_id(user['id'])
        return None
    
    def update_user_attribute(self, user_id : int = None, attributes : Dict[str, str] = {}) -> UserObject|None:

        if attributes == {}:
            logger.warning("No attributes were set to update.")
            return None
        
        logger.info(f"Updating user {user_id}...")

        r = RequestHandler.MakeRequest(
            mode=Mode.PATCH,
            url=f"{self.ctfd.ctfd_instance}/api/v1/users/{user_id}",
            token=self.ctfd.ctfd_token,
            json=attributes
        )

        if r.status_code == 404:
            logger.error(f"User with id {user_id} doesn't exist.")
            return None
    
        data = self.__request__(r, None, 200)
        if data == None:
            return None
        
        return UserObject(**data)
    
    def ban_user(self, user_id: int):
        return self.update_user_attribute(user_id=user_id, attributes={"banned": True})
    
    def unban_user(self, user_id: int):
        return self.update_user_attribute(user_id=user_id, attributes={"banned": False})
    
    def hide_user(self, user_id: int):
        return self.update_user_attribute(user_id=user_id, attributes={"hidden": True})
    
    def unhide_user(self, user_id: int):
        return self.update_user_attribute(user_id=user_id, attributes={"hidden": False})
    
    def delete_user(self, user_id: int) -> bool:
        logger.info(f"Deleting user {user_id}...")
        r = RequestHandler.MakeRequest(
            mode=Mode.DELETE,
            url=f"{self.ctfd.ctfd_instance}/api/v1/users/{user_id}",
            token=self.ctfd.ctfd_token
        )
        if r.status_code == 404:
            logger.error(f"User with id {user_id} doesn't exist.")
            return False        
        return True
    
    def create_user(self, name: str, password: str, email: str = "", team_id: int = None, role: str = "user", verified: bool = False, banned: bool = False, hidden: bool = False) -> UserObject|None:
    
            data = {
                    "name": name,
                    "password": password,
                    "team_id": team_id,
                    "role": role,
                    "verified": verified,
                    "banned": banned,
                    "hidden": hidden
                }
            
            if email != "":
                data["email"] = email

            logger.info(f"Creating user {name}...")
            r = RequestHandler.MakeRequest(
                mode=Mode.POST,
                url=f"{self.ctfd.ctfd_instance}/api/v1/users",
                token=self.ctfd.ctfd_token,
                json=data
            )
            if r.status_code == 400:
                logger.debug(f"Returned {r.json()}")
                logger.error(f"User with name {name} already exists.")
                return None
            
            data = self.__request__(r, None, 201)
            if data == None:
                return None
            
            return UserObject(**data)
    
    def create_user_from_dict(self, user_dict: dict) -> UserObject|None:
        return self.create_user(**user_dict)
    
    def add_user_to_team(self, user_id: int, team_id: int) -> UserObject|None:

        r = RequestHandler.MakeRequest(
            mode=Mode.GET,
            url=f"{self.ctfd.ctfd_instance}/api/v1/teams/{team_id}",
            token=self.ctfd.ctfd_token
        )
        if r.status_code == 404:
            logger.error(f"Team with id {team_id} doesn't exist.")
            return None

        up = self.update_user_attribute(user_id=user_id, attributes={"team_id": team_id})
        pprint(up)

        return up