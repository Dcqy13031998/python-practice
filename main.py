import json
import argparse
import os
from datetime import datetime
from argparse import ArgumentParser

def load_db(path):
    # loads a new json file to store the data, create new if doesn't exist
    try:
        # default is "r" -> read
        with open(path, 'r') as file:
            database = json.load(file)
            # file doesn't exist -> create empty database or file exist but empty or invalid 
    except (FileNotFoundError, json.JSONDecodeError):
        database = {}
    return database

# creates a new file if path dont exist
def save_db(database: dict[str:dict], path: str) -> None:
    with open(path, 'w') as file:
        json.dump(database, file, indent = 2, ensure_ascii = False)
    # save the data to json file


def add_task(database: dict[str, dict], description: str) -> None:
    # description = input() cant be use because it's inputting into a json file, need to use argparse
    now: str = datetime.now().strftime("%Y-%m-%dT%H:%M")
    # id automated
    uniqueid: int = str(int(max("0", *database.keys())) + 1)
    # createdat and updatedat automated with realtime datetime
    # status autoamted to not done
    database[uniqueid] = {
        "description" : description,
        "createdAt": now,
        "updatedAt": now,
        "status": "todo"
    }
    list_task({uniqueid: database[uniqueid]})


def delete_task(database: dict[str,dict], id: str) -> None:
    list_task({id: database[id]})
    # dictionaries use del
    print(f"You are deleting database{id}. Press 1 to proceed and 2 to return")
    choice = int(input())
    while choice not in [1,2]: 
        print("Invalid choice, please choose an option")
        choice = int(input())
    if choice == 1:
        del database[id]
        print(f"Task {id} deleted.")
    if choice == 2:
        print("Deletion Cancelled")

# Update time update not working
def update_task(database: dict[str,dict], id:str, description: str):
    # updatedat based on realtime usage of "update"
    now: str = datetime.now().strftime("%Y-%m-%dT%H:%M")
    database[id]["description"] = description 
    database[id]["updatedAt"] = now
    list_task({id: database[id]})

def list_task(database: dict[str,dict], status: str = 'all') -> None:
    # if not database:
    #     print("No Tasks available")

    print(f"{'ID':<5} {'Status': <15} {'Description': <30} {'createdAt': <20} {'updatedAt':<20}")
    print("-" * 95)
    table = []

    # if database[id] not in database:
    #     print(f"Task with id no.: {id} does not exist in the database.")
    
    for id, properties in database.items():
        if status == "all" or status == properties["status"]:
            # can be used for tabulate
            # table.append({
            #     "Id": id,
            #     "Status": properties["status"],
            #     "Description": properties["description"],
            #     "CreatedAt": datetime.fromisoformat(properties["createdat"]).strftime("%Y-%m-%dT%H:%M"),
            #     "UpdatedAt": datetime.fromisoformat(properties["updatedat"]).strftime("%Y-%m-%dT%H:%M")
            # })
            print(f"{id:<5} {properties['status']:<15} {properties['description']:<30} {properties['createdAt']:<20} {properties['updatedAt']:<20}")

# taskly mark 
def mark_task(database: dict[str,dict], id:str) -> None:
    print(f"Please choose a following status change: \n 1) Mark Done \n 2) Mark In Progress \n 3) Mark todo")
    choice = input()
    now: str = datetime.now().strftime("%Y-%m-%dT%H:%M")
    database[id]["updatedAt"] = now
    if choice == "1":
        database[id]["status"] = "done"
    if choice == "2":
        database[id]["status"] = "in-progress"
    if choice == "3":
        database[id]["status"] = "todo"
    else:
        print("Invalid choice! Status not changed.")

    list_task({id: database[id]})


def main() -> None:
    # ArgumentParser holds all the info necessary to parse command line into py data types
    parser = ArgumentParser(description="Taskly CLI")
    subparsers = parser.add_subparsers(dest = 'command', required = True)

    add_parser = subparsers.add_parser("add", help="Adding task to table")
    add_parser.add_argument("description", help="Description of the task")
    add_parser.set_defaults(func = add_task)

    del_parser = subparsers.add_parser("del", help="Delete a task")
    del_parser.add_argument('id', help='ID of the task')
    del_parser.set_defaults(func = delete_task)

    update_parser = subparsers.add_parser("update", help="Update description of a task")
    update_parser.add_argument('id',  help='ID of the task')
    update_parser.add_argument('description', help='New Description of the task')
    update_parser.set_defaults(func = update_task)

    list_parser = subparsers.add_parser("list", help="Listing all the task available")
    list_parser.add_argument('status', choices = ['all','todo', 'in-progress', 'done'], type = str.lower, help='All task regardless of status')
    list_parser.set_defaults(func = list_task)

    mark_parser = subparsers.add_parser("mark", help="Changing status of task")
    mark_parser.add_argument('id', help='id of task to change status')
    # mark_parser.add_argument('choice',choices = ['not done', 'in progress', 'done'],help='Choice of status change')
    mark_parser.set_defaults(func = mark_task)

    # parse_args parses arguments and returns as object with attribute
    args = parser.parse_args()

    database_path = os.path.expanduser("~/taskly.json")
    database = load_db(database_path)

    # vars() gives you a dictionary view of the objects attributes (especially things like Namespace).
    # dict() creates a new dictionary (from scratch or from data you provide).
    # unpack the args into a dict, removing "func"
    args_dict = vars(args).copy()
    func = args_dict.pop("func")
    args_dict.pop("command", None)

    # calling the function
    # means dictionary unpacking (**), each key-value pair in args_dict becomes a named argument in the function call.
    # use **args_dict same as 
    '''
    if args.command == "add":
        add_task(database, description=args.description)
    elif args.command == "delete":
        delete_task(database, id=args.id)
    '''

    func(database, **args_dict)
    save_db(database, database_path)


    # if args.func:
    #     args.func(args)
    # print(f'The task: {args.description} has been added')
    # if args.description:
    #     # "a" = append
    #     f = open("task.json", "a'")
    #     f.write(str(args) + '\n')

    # return list_task[func]

if __name__ == "__main__":
    main()

'''
id: A unique identifier for the task
description: A short description of the task
status: The status of the task (todo, in-progress, done)
createdAt: The date and time when the task was created
updatedAt: The date and time when the task was last updated
'''