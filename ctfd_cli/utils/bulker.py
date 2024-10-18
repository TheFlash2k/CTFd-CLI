import json
import csv
import yaml
import os

from .logger import logger
from ..ctfd import CTFd
from ..teams.team import TeamObject, TeamHandler
from ..users.user import UserObject, UserHandler

class BulkAdd(object):
    csv_fields = ["Name", "Email", "Member-1", "Member-2", "Member-3"]
    allowed_formats = ["json", "csv", "yaml"]

    def __init__(self, input_file: str, format: str, out_format, output_file: str, force=False, ctfd: CTFd = None):

        self.ctfd = ctfd
        self.force = force
        self.format = format
        self.input_file = input_file
        self.out_format = out_format
        self.output_file = output_file

        if not os.path.isfile(input_file):
            logger.error(f"Input file {input_file} does not exist.")
            exit(1)

        if os.path.isfile(output_file) and not self.force:
            logger.error(f"Output file {output_file} already exists. Use --force to overwrite.")
            exit(1)


        if self.out_format not in self.allowed_formats:
            logger.error(f"Invalid output format {out_format}. Must be one of: json, csv, yaml.")
            exit(1)

        if self.format not in self.allowed_formats:
            logger.error(f"Invalid format {format}. Must be one of: json, csv, yaml.")
            exit(1)

        if self.format == "json":
            self.data = json.load(open(input_file))

        elif self.format == "csv":
            self.data = []
            with open(input_file, "r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.data.append(row)

        elif self.format == "yaml":
            self.data = yaml.safe_load(open(input_file))

    def add(self):

        teams = []
        team_names = []
        team_emails = []
        logged = []
        

        for entry in self.data:
            team = TeamObject(**entry)

            if team.name in team_names:
                logger.error(f"Duplicate team name found: {team.name}")
                continue

            if team.email in team_emails:
                logger.error(f"Duplicate team email found: {team.email}")
                continue

            team_names.append(team.name)
            team_emails.append(team.email)
            teams.append(team)

        if os.path.isfile(self.output_file):
            with open(self.output_file, "r") as f:
                if self.out_format == "json":
                    for line in f:
                        data = json.loads(line)
                        logged.append(data["Name"])
                elif self.out_format == "csv":
                    reader = csv.DictReader(f)
                    for row in reader:
                        logged.append(row["Name"])
                elif self.out_format == "yaml":
                    for line in f:
                        data = yaml.safe_load(line)
                        logged.append(data["Name"])
        
        teams = [team for team in teams if team.name not in logged]
        logger.info(f"Found {len(teams)} teams to add (already wrote: {len(logged)} teams).")

        if not self.force:
            logger.error("Use --force to force add teams and discard duplicates.")
            exit(0)
            
        """
        To-DO:
        
        Check for duplicate members across teams.
        If there are any, modify the name as:
        <name>_<team_name>

        This is to avoid conflicts.
        """

        if not self.ctfd:
            logger.error("CTFd instance is not set.")

        th = TeamHandler(self.ctfd)
        uh = UserHandler(self.ctfd)

        if self.out_format == "csv":
            if not os.path.isfile(self.output_file):
                with open(self.output_file, "w") as f:
                    writer = csv.DictWriter(f, fieldnames=self.csv_fields)
                    writer.writeheader()

        for team in teams:
            info = {}

            """
            There was this one edge case where a person entered
            multiple emails in a single email field separated by a ,:
            """
            team.email = team.email.strip()
            team.name = team.name.strip().title()

            if "," in team.email:
                team.email = team.email.split(",")[0]

            info["Name"] = team.name
            info["Email"] = team.email
            info["members"] = []

            logger.debug("Adding team: " + team.name)
            if not (_team := th.create_team_from_dict(team.__dict__, return_if_exists = False, mode = TeamObject)):
                logger.error(f"Failed to create team {team.name}")

            logger.debug(f"Got team: {_team}")
            for i, member in enumerate(team.members):
                member.name = member.name.strip().title()
                logger.debug(f"Adding user: {member.name}")
                if not (_member := uh.create_user_from_dict(member.__dict__, return_if_exists=False)):
                    logger.error(f"Failed to create user {member.name}")
                    member.name = f"{member.name}_{team.name.replace(' ', '-')}"

                    if not (_member := uh.create_user_from_dict(member.__dict__, return_if_exists=False)):
                        logger.error(f"Failed to create user {member.name}")
                        continue
                
                logger.debug(f"Adding {member.name} to {_team.name}")
                th.add_member(_team.id, _member.id)

                info[f"members"].append({
                    "name": member.name,
                    "password": member.password
                })

            # We'll store info in output file.
            with open(self.output_file, "a") as f:
                if self.out_format == "json":
                    f.write(json.dumps(info) + "\n")
                elif self.out_format == "csv":
                    writer = csv.DictWriter(f, fieldnames=self.csv_fields)
                    member = info["members"]
                    for i in range(len(member)):
                        _member = member[i]
                        info[f"Member-{i+1}"] = f"{_member['name']}:{_member['password']}"
                    del info["members"]
                    writer.writerow(info)
                elif self.out_format == "yaml":
                    f.write(yaml.dump(info) + "\n")
            logger.info(f"Team {team.name} added successfully.")