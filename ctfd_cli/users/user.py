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
        if req.status_code != default_status_code and req.status_code != 200: # Just a hard-coded check.
            return default_ret_val
        try:
            data = req.json()['data']
        except KeyError:
            logger.error(f"An error occurred when parsing response: {req.json()}")
            return default_ret_val
        return data

    def get_all_users(self, mode=UserObject) -> List:

        if mode != UserObject and mode != dict:
            logger.error(f"Invalid mode {mode}")
            return []

        logger.info("Getting the list of all users...")
        r = RequestHandler.MakeRequest(
            mode=Mode.GET,
            url=f"{self.ctfd.ctfd_instance}/api/v1/users?view=admin",
            token=self.ctfd.ctfd_token
        )

        data = self.__request__(r, [])
        if data == []:
            return []
        
        users = []
        for user in data:
            users.append(UserObject(**user))

        if mode == UserObject:
            return users
        
        return [user.__dict__ for user in users]
      
    def get_user_by_id(self, id: int, mode=UserObject) -> UserObject|None:

        if mode != UserObject and mode != dict:
            logger.error(f"Invalid mode {mode}")
            return None

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
        
        if mode == dict:
            return data
        return UserObject(**data)

    def get_user_by_name(self, name : str, mode = UserObject) -> UserObject|None:

        logger.info(f"Getting info of user {name}")
        r = RequestHandler.MakeRequest(
            mode=Mode.GET,
            url=f"{self.ctfd.ctfd_instance}/api/v1/users?view=admin",
            token=self.ctfd.ctfd_token
        )

        data = self.__request__(r, None, 200)
        if data == None:
            return None
        
        for user in data:
            if user['name'] == name:
                logger.info(f"User {name} has the ID {user['id']}")
                return self.get_user_by_id(user['id'], mode=mode)
        return None
    
    def update_user_attribute(self, id : int = None, attributes : Dict[str, str] = {}, mode=UserObject) -> UserObject|None:

        if mode != UserObject and mode != dict:
            logger.error(f"Invalid mode {mode}")
            return None

        if attributes == {}:
            logger.warning("No attributes were set to update.")
            return None
        
        logger.info(f"Updating user {id}...")

        r = RequestHandler.MakeRequest(
            mode=Mode.PATCH,
            url=f"{self.ctfd.ctfd_instance}/api/v1/users/{id}",
            token=self.ctfd.ctfd_token,
            json=attributes
        )

        if r.status_code == 404:
            logger.error(f"User with id {id} doesn't exist.")
            return None
    
        data = self.__request__(r, None, 200)
        if data == None:
            return None
        
        if mode == dict:
            return data
        return UserObject(**data)
    
    def ban_user(self, id: int):
        return self.update_user_attribute(id=id, attributes={"banned": True})
    
    def unban_user(self, id: int):
        return self.update_user_attribute(id=id, attributes={"banned": False})
    
    def hide_user(self, id: int):
        return self.update_user_attribute(id=id, attributes={"hidden": True})
    
    def unhide_user(self, id: int):
        return self.update_user_attribute(id=id, attributes={"hidden": False})
    
    def delete_user(self, id: int) -> bool:
        logger.info(f"Deleting user {id}...")
        r = RequestHandler.MakeRequest(
            mode=Mode.DELETE,
            url=f"{self.ctfd.ctfd_instance}/api/v1/users/{id}",
            token=self.ctfd.ctfd_token
        )
        if r.status_code == 404:
            logger.error(f"User with id {id} doesn't exist.")
            return False        
        return True
    
    def create_user(self, name: str, password: str, email: str = "", team_id: int = None, role: str = "user", verified: bool = False, banned: bool = False, hidden: bool = False, mode=UserObject, return_if_exists=True, **kwargs) -> UserObject|None:

        if mode != UserObject and mode != dict:
            logger.error(f"Invalid mode {mode}")
            return None

        data = {
                "name": name,
                "password": password,
                "team_id": team_id,
                "role": role,
                "verified": verified,
                "banned": banned,
                "hidden": hidden,
                "affiliation": kwargs.get("affiliation", None),
            }
        
        if email:
            data["email"] = email

        logger.info(f"Creating user {name}...")
        r = RequestHandler.MakeRequest(
            mode=Mode.POST,
            url=f"{self.ctfd.ctfd_instance}/api/v1/users",
            token=self.ctfd.ctfd_token,
            json=data
        )
        if r.status_code == 400:
            logger.error(f"User with name {name} might already exists. [Error: {r.json()['errors']}]")
            return self.get_user_by_name(name) if return_if_exists else None
        
        data = self.__request__(r, None, 201)
        if data == None:
            return None
        
        if mode == dict:
            return data

        return UserObject(**data)
    
    def create_user_from_dict(self, user_dict: dict, return_if_exists: bool = True,  mode : object = UserObject) -> UserObject|None:
        return self.create_user(**user_dict, mode=mode, return_if_exists=return_if_exists)
    
    def add_user_to_team(self, id: int, team_id: int) -> UserObject|None:

        r = RequestHandler.MakeRequest(
            mode=Mode.GET,
            url=f"{self.ctfd.ctfd_instance}/api/v1/teams/{team_id}",
            token=self.ctfd.ctfd_token
        )
        if r.status_code == 404:
            logger.error(f"Team with id {team_id} doesn't exist.")
            return None

        up = self.update_user_attribute(id=id, attributes={"team_id": team_id})
        return up
