class UserObject:
    def __set_val__(self, value, default=None):
        if not hasattr(self, value):
            setattr(self, value, default)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        try:
            self.__set_val__("banned", False)
            self.__set_val__("hidden", False)
            self.__set_val__("email", None)
            self.__set_val__("team_id", None)

            return f"CTFd-User({f'[HIDDEN] ' if self.hidden else ''}{f'[BANNED] ' if self.banned else ''}id={self.id}, name={self.name}, team_id={self.team_id})"
        except Exception as E:
            return "CTFd-User(?)"
    
    def __repr__(self):
        return self.__str__()

    
class TeamObject:
    def __set_val__(self, value, default=None):
        if not hasattr(self, value):
            setattr(self, value, default)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        try:
            self.__set_val__("banned", False)
            self.__set_val__("hidden", False)
            r = f"CTFd-Team(id={self.id}, name={self.name}"
            if hasattr(self, "members"):
                r += f", members={self.members}"
            r += ")"
            r += f"{'[HIDDEN] ' if self.hidden else ''}{f'[BANNED] ' if self.banned else ''}"
            return r
        except:
            return "CTFd-Team(?)"
    
    def __repr__(self):
        return self.__str__()