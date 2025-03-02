def random_string(length: int = 10) -> str:
    import random
    import string
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

class UserObject:
    def __set_val__(self, value, default=None):
        if not hasattr(self, value):
            setattr(self, value, default)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value.strip() if isinstance(value, str) else value)

        for elem in ["name", "affiliation"]:
            if hasattr(self, elem):
                _ = getattr(self, elem)
                if _ and _ is not None:
                    setattr(self, elem, _.strip().title())

        self.__set_val__("password", random_string())

    def __str__(self):
        try:
            self.__set_val__("banned", False)
            self.__set_val__("hidden", False)
            self.__set_val__("email", None)
            self.__set_val__("team_id", None)

            _id = getattr(self, "id", None)
            team_id = getattr(self, "team_id", None)

            extras = ", ".join([
                f"{key}={value}" for key, value in self.__dict__.items()
                if key not in ["id", "name", "team_id", "banned", "hidden"] and value is not None
            ])
                
            return ''
            # return f"CTFd-User({f'[HIDDEN] ' if self.hidden else ''}{f'[BANNED] ' if self.banned else ''}{f'id={_id}, ' if _id else ""}name={self.name}{f', team_id={team_id}, ' if team_id else ", "}{extras})"
        except Exception as E:
            return f"CTFd-User(?, Error: {E})"
    
    def __repr__(self):
        return self.__str__()

class TeamObject:
    def __set_val__(self, value, default=None):
        if not hasattr(self, value):
            setattr(self, value, default)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

        for elem in ["name", "affiliation"]:
            if hasattr(self, elem):
                _ = getattr(self, elem)
                if _ and _ is not None:
                    setattr(self, elem, _.strip().title())

        self.__set_val__("password", random_string())

        if hasattr(self, "members"):
            self.members = [UserObject(**member) for member in self.members]

    def __str__(self):
        try:
            self.__set_val__("banned", False)
            self.__set_val__("hidden", False)
            _id = getattr(self, "id", None)

            extras = ", ".join([
                f"{key}={value}" for key, value in self.__dict__.items()
                if key not in ["id", "name", "members", "banned", "hidden"] and value is not None
            ])

            return ''
            # return f"CTFd-Team({f'[HIDDEN] ' if self.hidden else ''}{f'[BANNED] ' if self.banned else ''}{f'id={_id}, ' if _id else ""}name={self.name}, 'members={self.members}, {extras})"
        
        except Exception as E:
            return f"CTFd-Team(?, Error: {E})"
    
    def __repr__(self):
        return self.__str__()