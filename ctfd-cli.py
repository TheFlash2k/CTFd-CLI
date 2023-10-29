#!/usr/bin/env python3

import argparse
from pprint import pprint
import json

from ctfd_cli import CTFd
from ctfd_cli.utils.logger import logger
from ctfd_cli.users.user import UserHandler


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

team_parser = subparsers.add_parser('team', help='Team mode')

args = parser.parse_args()

ctfd = CTFd(args.ctfd_instance, args.ctfd_token)
uh = UserHandler(ctfd)

if args.mode == "user":
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
    else:
        logger.error(f"Invalid user mode {args.user_mode}")
        exit(1)

elif args.mode == "team":
    pass
