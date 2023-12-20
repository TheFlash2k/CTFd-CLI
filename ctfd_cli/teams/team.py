from ..utils.logger import logger
from ..schemas import TeamObject
from ..utils.handler import RequestHandler, Mode
from ..ctfd import CTFd

from typing import List, Dict
from pprint import pprint

class TeamHandler:
    
    def __init__(self, ctfd: CTFd):
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

    def get_all_teams(self, mode=TeamObject) -> List:

        if mode != TeamObject and mode != dict:
            logger.error(f"Invalid mode {mode}")
            return []

        logger.info("Getting the list of all teams...")
        r = RequestHandler.MakeRequest(
            mode=Mode.GET,
            url=f"{self.ctfd.ctfd_instance}/api/v1/teams?view=admin",
            token=self.ctfd.ctfd_token
        )

        data = self.__request__(r, [])
        if data == []:
            return []
        
        teams = []

        for team in data:
            teams.append(TeamObject(**team))

        if mode == TeamObject:
            return teams
        
        return [team.__dict__ for team in teams]
    
    def get_team_by_id(self, id: int, mode=TeamObject) -> TeamObject|dict|None:
            
            if mode != TeamObject and mode != dict:
                logger.error(f"Invalid mode {mode}")
                return None
    
            if id == None:
                return None
    
            logger.info(f"Getting info of team {id}")
            r = RequestHandler.MakeRequest(
                mode=Mode.GET,
                url=f"{self.ctfd.ctfd_instance}/api/v1/teams/{id}?view=admin",
                token=self.ctfd.ctfd_token
            )
    
            data = self.__request__(r, None)
            if data == None:
                return None
            
            team = TeamObject(**data)
    
            if mode == TeamObject:
                return team
            
            return team.__dict__
    
    def get_team_by_name(self, name: str, mode=TeamObject) -> TeamObject|None:
                
        if mode != TeamObject and mode != dict:
            logger.error(f"Invalid mode {mode}")
            return None

        if name == None:
            return None

        logger.info(f"Getting info of team {name}")
        r = RequestHandler.MakeRequest(
            mode=Mode.GET,
            url=f"{self.ctfd.ctfd_instance}/api/v1/teams?view=admin",
            token=self.ctfd.ctfd_token
        )

        data = self.__request__(r, None)
        if data == None:
            return None
        
        for team in data:
            if team['name'] == name:
                team = TeamObject(**team)
                if mode == TeamObject:
                    return team
                return team.__dict__
        
        return None
        
        return team.__dict__

    def update_team_attribute(self, id: int = None, attributes : Dict[str, str] = {}, req_mode: Mode = Mode.PATCH, endpoint: str = "", mode = TeamObject) -> TeamObject|None:

        if mode != TeamObject and mode != dict:
            logger.error(f"Invalid mode {mode}")
            return None

        if id == None:
            return None

        logger.info(f"Updating team {id} with attributes {attributes}")
        r = RequestHandler.MakeRequest(
            mode=req_mode,
            url=f"{self.ctfd.ctfd_instance}/api/v1/teams/{id}{endpoint}",
            token=self.ctfd.ctfd_token,
            json=attributes
        )

        data = self.__request__(r, None)
        if data == None:
            return None
        
        try:
            team = TeamObject(**data)

            if mode == TeamObject:
                return team
            
            return team.__dict__
        except:
            return data
    
    def create_team(self, name: str, password: str, email: str = None, affiliation: str = None, website: str = None, country: str = None, mode=TeamObject) -> TeamObject|None:

        if mode != TeamObject and mode != dict:
            logger.error(f"Invalid mode {mode}")
            return None

        if name == None:
            return None
        
        data= {
            "name": name,
            "password": password,
            "affiliation": affiliation,
            "website": website,
            "country": country
        }

        if email:
            data['email'] = email

        logger.info(f"Creating team {name}...")
        r = RequestHandler.MakeRequest(
            mode=Mode.POST,
            url=f"{self.ctfd.ctfd_instance}/api/v1/teams",
            token=self.ctfd.ctfd_token,
            json=data
        )

        data = self.__request__(r, None, 200)

        if r.status_code == 400:
            logger.error(f"Team with name {name} already exists.")
            return self.get_team_by_name(name)

        if data == None:
            return None
        
        team = TeamObject(**data)

        if mode == TeamObject:
            return team
        
        return team.__dict__
    
    def create_team_from_dict(self, team_dict: dict, mode=TeamObject) -> TeamObject|None:
        return self.create_team(**team_dict)
    
    def delete_team(self, id: int) -> bool:
        logger.info(f"Deleting team {id}...")
        r = RequestHandler.MakeRequest(
            mode=Mode.DELETE,
            url=f"{self.ctfd.ctfd_instance}/api/v1/teams/{id}",
            token=self.ctfd.ctfd_token
        )
        if r.status_code == 404:
            logger.error(f"Team with id {id} doesn't exist.")
            return False        
        return True
    
    def add_member(self, id: int, user_id: int, mode=TeamObject) -> TeamObject|None:
            
        r = RequestHandler.MakeRequest(
            mode=Mode.GET,
            url=f"{self.ctfd.ctfd_instance}/api/v1/teams/{id}",
            token=self.ctfd.ctfd_token
        )

        data = self.__request__(r, None)
        if data == None:
            return None
        
        members = data.get("members", [])
        if user_id in members:
            logger.error(f"User {user_id} is already in team {id}")
            return None
        
        return self.update_team_attribute(id, attributes={"user_id": user_id}, req_mode=Mode.POST, endpoint="/members", mode=mode)
    
    def remove_member(self, id: int, user_id: int, mode=TeamObject) -> bool:

        members = self.get_team_members(id)
        if members == None:
            return None
        
        if user_id not in members:
            logger.error(f"User {user_id} is not in team {id}")
            return None

        return self.update_team_attribute(id, attributes={"user_id": user_id}, req_mode=Mode.DELETE, endpoint="/members", mode=mode) != None
    
    def get_team_members(self, id: int) -> List:
                    
        r = RequestHandler.MakeRequest(
            mode=Mode.GET,
            url=f"{self.ctfd.ctfd_instance}/api/v1/teams/{id}",
            token=self.ctfd.ctfd_token
        )

        data = self.__request__(r, None)
        if data == None:
            return None
        return data.get("members", [])
    
    def ban_team(self, id: int, mode=TeamObject) -> TeamObject|None:
        return self.update_team_attribute(id, {"banned": True}, mode=mode)
    
    def unban_team(self, id: int, mode=TeamObject) -> TeamObject|None:
        return self.update_team_attribute(id, {"banned": False}, mode=mode)
    
    def hide_team(self, id: int, mode=TeamObject) -> TeamObject|None:
        return self.update_team_attribute(id, {"hidden": True}, mode=mode)
    
    def unhide_team(self, id: int, mode=TeamObject) -> TeamObject|None:
        return self.update_team_attribute(id, {"hidden": False}, mode=mode)
