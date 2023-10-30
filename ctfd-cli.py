#!/usr/bin/env python3

import argparse
from pprint import pprint
import json

from ctfd_cli import CTFd
from ctfd_cli.utils.logger import logger
from ctfd_cli.users.user import UserHandler
from ctfd_cli.teams.team import TeamHandler
from ctfd_cli.utils.parser import Parser


parser = argparse.ArgumentParser(description='CTFd CLI')
parser.add_argument('--ctfd-instance', type=str, help='CTFd instance URL', default=None)
parser.add_argument('--ctfd-token', type=str, help='CTFd admin token', default=None)
subparsers = parser.add_subparsers(required=True, dest='mode')

user_parser = subparsers.add_parser('user', help='User mode')
user_subparsers = user_parser.add_subparsers(required=True, dest='user_mode')

user_create_parser = user_subparsers.add_parser('create', help='Create user')
user_create_parser.add_argument('--name', type=str, help='Username', required=True)
user_create_parser.add_argument('--password', type=str, help='Password', required=True)
user_create_parser.add_argument('--email', type=str, help='Email', default="")
user_create_parser.add_argument('--team-id', type=int, help='Team ID', default=None)
user_create_parser.add_argument('--role', type=str, help='Role', default="user")
user_create_parser.add_argument('--verified', type=bool, help='Verified', default=False)
user_create_parser.add_argument('--banned', type=bool, help='Banned', default=False)
user_create_parser.add_argument('--hidden', type=bool, help='Hidden', default=False)
user_delete_parser = user_subparsers.add_parser('delete', help='Delete user')
user_delete_parser.add_argument('--user-id', type=int, help='User ID', required=True)
user_update_parser = user_subparsers.add_parser('update', help='Update user')
user_update_parser.add_argument('--user-id', type=int, help='User ID', required=True)
user_update_parser.add_argument('--attributes', type=str, help='Attributes (passed as a json object)')
user_update_parser.add_argument('--attributes-json', type=str, help='Attributes json file')
user_get_parser = user_subparsers.add_parser('get', help='Get user')
user_get_parser.add_argument('--user-id', type=int, help='User ID', required=True)
user_list_parser = user_subparsers.add_parser('list', help='List users')
user_ban_parser = user_subparsers.add_parser('ban', help='Ban user')
user_ban_parser.add_argument('--user-id', type=int, help='User ID', required=True)
user_unban_parser = user_subparsers.add_parser('unban', help='Unban user')
user_unban_parser.add_argument('--user-id', type=int, help='User ID', required=True)
user_hide_parser = user_subparsers.add_parser('hide', help='Hide user')
user_hide_parser.add_argument('--user-id', type=int, help='User ID', required=True)
user_unhide_parser = user_subparsers.add_parser('unhide', help='Unhide user')
user_unhide_parser.add_argument('--user-id', type=int, help='User ID', required=True)

team_parser = subparsers.add_parser('team', help='Team mode')
team_subparsers = team_parser.add_subparsers(required=True, dest='team_mode')

team_create_parser = team_subparsers.add_parser('create', help='Create team')
team_create_parser.add_argument('--name', type=str, help='Team name', required=True)
team_create_parser.add_argument('--password', type=str, help='Team password', required=True)
team_create_parser.add_argument('--email', type=str, help='Team email', default="")
team_create_parser.add_argument('--affiliation', type=str, help='Team affiliation', default="")
team_create_parser.add_argument('--country', type=str, help='Team country', default="")

team_add_member_parser = team_subparsers.add_parser('add-member', help='Add member to team')
team_add_member_parser.add_argument('--team-id', type=int, help='Team ID', required=True)
team_add_member_parser.add_argument('--user-id', type=int, help='User ID')
team_add_member_parser.add_argument('--user-ids', type=str, help='List of User IDs (comma separated)')

team_del_member_parser = team_subparsers.add_parser('del-member', help='Remove member from team')
team_del_member_parser.add_argument('--team-id', type=int, help='Team ID', required=True)
team_del_member_parser.add_argument('--user-id', type=int, help='User ID')
team_del_member_parser.add_argument('--user-ids', type=str, help='List of User IDs (comma separated)')

team_delete_parser = team_subparsers.add_parser('delete', help='Delete team')
team_delete_parser.add_argument('--team-id', type=int, help='Team ID', required=True)

team_update_parser = team_subparsers.add_parser('update', help='Update team')
team_update_parser.add_argument('--team-id', type=int, help='Team ID', required=True)
team_update_parser.add_argument('--attributes', type=str, help='Attributes (passed as a json object)')
team_update_parser.add_argument('--attributes-json', type=str, help='Attributes json file')

team_get_parser = team_subparsers.add_parser('get', help='Get team')
team_get_parser.add_argument('--team-id', type=int, help='Team ID', required=True)
team_list_parser = team_subparsers.add_parser('list', help='List teams')

bulker_parser = subparsers.add_parser('bulk-add', help="Add team and users in bulk (using csv, json and yaml files)")
bulker_parser.add_argument('--csv-file', type=str, help="CSV File to add teams from (Check samples/sample.csv)")
bulker_parser.add_argument('--json-file', type=str, help="JSON File to add teams from (Check samples/sample.json)")
bulker_parser.add_argument('--yaml-file', type=str, help="YAML File to add teams from (Check samples/sample.yaml)")
bulker_parser.add_argument('--output-format', type=str, help="Output format, can be json, yaml or csv", default="json", choices=["json", "yaml", "csv"])
bulker_parser.add_argument('--output-file', type=str, help="Output file, if not specified, will be printed to stdout")

parser_parser = subparsers.add_parser('parse', help='Parse a CSV file into a format that CTFD-CLI will understand (currently works only with Google Forms csv sheets)')
parser_parser.add_argument('--csv-file', type=str, help="CSV File to parse (Check samples/sample.csv)")
parser_parser.add_argument('--output-format', type=str, help="Output format, can be json, yaml or csv", default="csv", choices=["json", "yaml", "csv"])
parser_parser.add_argument('--output-file', type=str, help="Output file, if not specified, will be printed to stdout", default="output.csv")

args = parser.parse_args()

ctfd = CTFd(args.ctfd_instance, args.ctfd_token)

if args.mode == "user":
    uh = UserHandler(ctfd)
    if args.user_mode == "create":
        user = uh.create_user(
            name=args.name,
            password=args.password,
            email=args.email,
            team_id=args.team_id,
            role=args.role,
            verified=args.verified,
            banned=args.banned,
            hidden=args.hidden
        )
        if user == None:
            logger.error(f"Failed to create user {args.name}")
            exit(1)
        logger.info(f"Created user {user}")
    elif args.user_mode == "delete":
        if uh.delete_user(id=args.user_id):
            logger.info(f"Deleted user {args.user_id}")
        else:
            logger.error(f"Failed to delete user {args.user_id}")
            exit(1)
    elif args.user_mode == "update":

        if args.attributes == None and args.attributes_json == None:
            logger.error(f"No attributes were set to update.")
            exit(1)

        if args.attributes_json != None:
            try:
                with open(args.attributes_json, "r") as f:
                    args.attributes = f.read()
            except FileNotFoundError:
                logger.error(f"File {args.attributes_json} not found")
                exit(1)

        if args.attributes == None:
            logger.error(f"No attributes were set to update.")
            exit(1)

        try:
            attr = json.loads(args.attributes)
        except json.decoder.JSONDecodeError:
            logger.error(f"Invalid attributes {args.attributes}")
            exit(1)
        user = uh.update_user_attribute(id=args.user_id, attributes=attr, mode=dict)
        if user == None:
            logger.error(f"Failed to update user {args.user_id}")
            exit(1)
        logger.info(f"Updated user {user}")
    elif args.user_mode == "get":
        user = uh.get_user_by_id(id=args.user_id, mode=dict)
        if user == None:
            logger.error(f"Failed to get user {args.user_id}")
            exit(1)
        logger.info(f"Got user {user}")
    elif args.user_mode == "list":
        users = uh.get_all_users(mode=dict)
        if users == None:
            logger.error(f"Failed to get users")
            exit(1)
        pprint(users)
    elif args.user_mode == "ban":
        if uh.ban_user(id=args.user_id):
            logger.info(f"Banned user {args.user_id}")
        else:
            logger.error(f"Failed to ban user {args.user_id}")
            exit(1)
    elif args.user_mode == "unban":
        if uh.unban_user(id=args.user_id):
            logger.info(f"Unbanned user {args.user_id}")
        else:
            logger.error(f"Failed to unban user {args.user_id}")
            exit(1)
    elif args.user_mode == "hide":
        if uh.hide_user(id=args.user_id):
            logger.info(f"Hid user {args.user_id}")
        else:
            logger.error(f"Failed to hide user {args.user_id}")
            exit(1)
    elif args.user_mode == "unhide":
        if uh.unhide_user(id=args.user_id):
            logger.info(f"Unhid user {args.user_id}")
        else:
            logger.error(f"Failed to unhide user {args.user_id}")
            exit(1)
    else:
        logger.error(f"Invalid user mode {args.user_mode}")
        exit(1)

elif args.mode == "team":
    th = TeamHandler(ctfd)
    if args.team_mode == "create":
        team = th.create_team(
            name=args.name,
            password=args.password,
            email=args.email,
            affiliation=args.affiliation,
            country=args.country,
        )
        if team == None:
            logger.error(f"Failed to create team {args.name}")
            exit(1)
        logger.info(f"Created team {team}")
    elif args.team_mode == "delete":
        if th.delete_team(id=args.team_id):
            logger.info(f"Deleted team {args.team_id}")
        else:
            logger.error(f"Failed to delete team {args.team_id}")
            exit(1)
    elif args.team_mode == "update":

        if args.attributes == None and args.attributes_json == None:
            logger.error(f"No attributes were set to update.")
            exit(1)

        if args.attributes_json != None:
            try:
                with open(args.attributes_json, "r") as f:
                    args.attributes = f.read()
            except FileNotFoundError:
                logger.error(f"File {args.attributes_json} not found")
                exit(1)

        if args.attributes == None:
            logger.error(f"No attributes were set to update.")
            exit(1)

        try:
            attr = json.loads(args.attributes)
        except json.decoder.JSONDecodeError:
            logger.error(f"Invalid attributes {args.attributes}")
            exit(1)
        team = th.update_team_attribute(id=args.team_id, attributes=attr, mode=dict)
        if team == None:
            logger.error(f"Failed to update team {args.team_id}")
            exit(1)
        logger.info(f"Updated team {team}")
    elif args.team_mode == "get":
        team = th.get_team_by_id(id=args.team_id, mode=dict)
        if team == None:
            logger.error(f"Failed to get team {args.team_id}")
            exit(1)
        logger.info(f"Got team {team}")
    elif args.team_mode == "list":
        teams = th.get_all_teams(mode=dict)
        if teams == None:
            logger.error(f"Failed to get teams")
            exit(1)
        pprint(teams)
    elif args.team_mode == "add-member":
        if args.user_id != None:
            user_ids = [args.user_id]
        elif args.user_ids != None:
            user_ids = args.user_ids.split(",")
        else:
            logger.error(f"Please specify either --user-id or --user-ids")
            exit(1)

        for user_id in user_ids:
            if th.add_member(id=args.team_id, user_id=user_id):
                logger.info(f"Added user {user_id} to team {args.team_id}")
            else:
                logger.error(f"Failed to add user {user_id} to team {args.team_id}")
                exit(1)
    elif args.team_mode == "del-member":
        if args.user_id != None:
            user_ids = [args.user_id]
        elif args.user_ids != None:
            user_ids = args.user_ids.split(",")
        else:
            logger.error(f"Please specify either --user-id or --user-ids")
            exit(1)

        for user_id in user_ids:
            if th.remove_member(id=args.team_id, user_id=user_id):
                logger.info(f"Removed user {user_id} from team {args.team_id}")
            else:
                logger.error(f"Failed to remove user {user_id} from team {args.team_id}")
                exit(1)
    else:
        logger.error(f"Invalid team mode {args.team_mode}")
        exit(1)

elif args.mode == "bulk-add":
    logger.info("Currently under development.")
    pass

elif args.mode == "parse":

    if args.csv_file == None:
        logger.error(f"Please specify a csv file to parse")
        exit(1)

    p = Parser(file=args.csv_file, out_file=args.output_file, out_mode=args.output_format)
    _teams = p.parse(store=True)
    pprint(_teams)