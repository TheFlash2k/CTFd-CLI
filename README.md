# CTFd-CLI
A Command Line Utility to perform actions with a CTFd Instance using the CTFd REST API

---

In order to interact with the CTFd API, you need to have an API key and the IP/Hostname of the CTFd instance. These can be configured inside the `.env` file.
For starters, you can copy the `.env.example` file and rename it to `.env` and fill in the values.

## Usage

You have the following available commands:

- `ctfd-cli users` - List all users
- `ctfd-cli user <COMMANDS>` - Perform an action to a user
