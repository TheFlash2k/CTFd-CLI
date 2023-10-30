import json
import yaml
import csv
from .logger import logger
from pprint import pprint

class Parser:

    def __file__(self):
        _i = False
        try:
            if not self.in_file:
                raise Exception("No file provided.")
            with open(self.in_file, "r") as f:
                if f.read() != "":
                    _i = True
            if not self.out_file:
                return True
            with open(self.out_file, "w") as f:
                return (True and _i)
        except Exception as E:
            raise E

    def __init__(self, file, out_file = "output.csv", out_mode="csv"):
        self.in_file = file
        self.out_file = out_file
        self.out_mode = out_mode
        self.__file__() # File checking...
        self.data = {}

    def google_forms(self, store=True) -> dict:

        valid_fields = [
            { "team_name" : True },
            { "team_password" : False },
            { "team_affiliation" : False },
            { "team_email" : False },
            { "user_name" : True },
            { "user_email" : False },
            { "user_affiliation" : False },
            { "user_password" : False },
        ]

        t_fields = ""
        for i in valid_fields:
            if not list(i.values())[0]:
                t_fields += "*"
            t_fields += list(i.keys())[0] + ", "

        print(f"""Valid fields: {t_fields}
NOTE: Fields with * are optional. Rest are important.
              
Example::
Let's say you're google forms csv is:
              
Timestamp,Team Name,Team Member 1 - Name, Team Member 2 - Name
10/30/2023 17:50:19, AirOverflow, TheFlash2k, Hash3lizer

The first field i.e. timestamp will automatically be skipped. Your form field will be:
team_name,user_name

Similarly:
Timestamp,Team Name,Team Member 1 - Name, Team Member 1 - Email, Team Member 2 - Name, Team Member 2 - Email
10/30/2023 17:50:19, AirOverflow, TheFlash2k, root@theflash2k.me, Hash3lizer, info@shameerkashif.me

This will be:
team_name,user_name,user_email
""")
        fields = input("Enter form fields seperated by a comma\n>> ")
        if not fields:
            logger.error("No fields entered.")
            return False
        fields = fields.replace(' ','').split(",")

        if len(fields) < 2:
            logger.error("Atleast 2 fields are required.")
            return False
        
        for i in fields:
            if i not in [list(i.keys())[0] for i in valid_fields]:
                logger.error(f"Invalid field {i}")
                return False
            
        for i in valid_fields:
            if list(i.values())[0] and list(i.keys())[0] not in fields:
                logger.error(f"Required field {list(i.keys())[0]} is missing.")
                return False
            
        if len(fields) != len(set(fields)):
            logger.error("Duplicate fields found.")
            return False
        
        with open(self.in_file, "r") as f:
            reader = csv.reader(f)
            self.data = list(reader)
            self.data = [i[1:] for i in self.data[1:]]

        teamname_idx = fields.index("team_name")
        teams = {}
        
        for i in self.data:
            teams[i[teamname_idx]] = {}

            for j in fields:
                if j.startswith("team_") and j != "team_name":
                    teams[i[teamname_idx]][j.replace("team_", '')] = i[fields.index(j)]
            
            user_fields = {}
            for j in fields:
                if j.startswith("user_"):
                    user_fields[j] = fields.index(j)

            teams[i[teamname_idx]]["members"] = []

            idxs = []
            for j in user_fields:
                idxs.append(user_fields[j] - 1)

            start = min(idxs) + 1
            diff  = (max(idxs) - start) + 2

            for j in range(start, len(i), diff):
                user = i[j:j+diff]
                user_fields = {}
                for k in fields:
                    if k.startswith("user_"):
                        try:
                            user_fields[k.replace("user_",'')] = user[fields.index(k) - start]
                        except IndexError:
                            pass

                name = user_fields["name"]
                del user_fields["name"]
                if user_fields == {}:
                    teams[i[teamname_idx]]["members"].append(name)
                else:
                    teams[i[teamname_idx]]["members"].append({name: user_fields})
        if store:
            if self.out_mode == "json":
                with open(self.out_file, "w") as f:
                    f.write(json.dumps(teams, indent=4))

            elif self.out_mode == "yaml":
                with open(self.out_file, "w") as f:
                    f.write(yaml.dump(teams, indent=4))
            
            elif self.out_mode == "csv":
                with open(self.out_file, "w", newline='') as f:
                    writer = csv.writer(f)
                    for i in teams:
                        team_str = i
                        members = []
                        for j in teams[i]:
                            if j != "members":
                                team_str += f":{j}={teams[i][j]}"
                            else:
                                for member in teams[i][j]:
                                    if type(member) == str:
                                        members.append(member)
                                    else:
                                        for name, items in member.items():
                                            member_str = name
                                            for k in items:
                                                member_str += f":{k}={items[k]}"
                                            members.append(member_str)
                                    
                        csv_str = f"{team_str},{','.join(members)}"
                        # writer.writerow adds an extra newline
                        writer.writerow(csv_str.split(","))
            else:
                logger.error(f"Invalid output mode {self.out_mode}")
                return False
            
            print(f"Output saved to {self.out_file}")
        return teams
    
    def parse(self, store=True) -> dict:
        return self.google_forms(store=store)