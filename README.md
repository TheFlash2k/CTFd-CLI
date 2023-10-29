# CTFd-CLI

A Command Line Utility to perform actions with a CTFd Instance using the CTFd REST API.

---

In order to interact with the CTFd API, you need to have an API key and the IP/Hostname of the CTFd instance. These can be configured inside the `.env` file.
For starters, you can copy the `.env.example` file and rename it to `.env` and fill in the values.

## Usage

```bash
usage: ctfd-cli.py [-h] [--ctfd-instance CTFD_INSTANCE] [--ctfd-token CTFD_TOKEN] {user,team} ...

CTFd CLI

positional arguments:
  {user,team}
    user                User mode
    team                Team mode

options:
  -h, --help            show this help message and exit
  --ctfd-instance CTFD_INSTANCE
                        CTFd instance URL
  --ctfd-token CTFD_TOKEN
                        CTFd admin token
```

### User mode

```bash
usage: ctfd-cli.py user [-h] {create,delete,update,get,list}

positional arguments:
  {create,delete,update,get,list}
    create              Create user
    delete              Delete user
    update              Update user
    get                 Get user
    list                List users

options:
  -h, --help            show this help message and exit
```

- Create user:

```bash
usage: ctfd-cli.py user create [-h] --name NAME --password PASSWORD [--email EMAIL] [--team-id TEAM_ID] [--role ROLE]
                               [--verified VERIFIED] [--banned BANNED] [--hidden HIDDEN]

options:
  -h, --help           show this help message and exit
  --name NAME          Username [required]
  --password PASSWORD  Password [required]
  --email EMAIL        Email
  --team-id TEAM_ID    Team ID
  --role ROLE          Role
  --verified VERIFIED  Verified
  --banned BANNED      Banned
  --hidden HIDDEN      Hidden
```

- Delete user:

```bash
usage: ctfd-cli.py user delete [-h] --user-id USER_ID

options:
  -h, --help         show this help message and exit
  --user-id USER_ID  User ID
```

- Update user:

```bash
usage: ctfd-cli.py user update [-h] --user-id USER_ID [--attributes ATTRIBUTES] [--attributes-json ATTRIBUTES_JSON]

options:
  -h, --help            show this help message and exit
  --user-id USER_ID     User ID
  --attributes ATTRIBUTES
                        Attributes (passed as a json object)
  --attributes-json ATTRIBUTES_JSON
                        Attributes json file
```

The update attributes can be plain json object passed from the command-line as follows:

```bash
python3 ctfdcli.py user update --attributes '{"banned": true, "hidden": false}'
```

Or you can pass a json file containing the attributes:

```json: attributes.json
{
    "banned": true,
    "hidden": false
}
```

```bash
python3 ctfdcli.py user update --attributes-json attributes.json
```

- Get user:

```bash
usage: ctfd-cli.py user get [-h] --user-id USER_ID
```

- List users:

Get a list of all users (Only those that have 'hidden=false' and 'banned=false')

```bash
usage: ctfd-cli.py user list
```

### Team mode

> Currently under development.

---
