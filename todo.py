import random
import json
from colorama import Fore, Style, init

init()

class c:
    def __init__(self):
        self.red = Fore.RED
        self.green = Fore.GREEN
        self.yellow = Fore.YELLOW
        self.blue = Fore.BLUE
        self.magenta = Fore.MAGENTA
        self.cyan = Fore.CYAN
        self.white = Fore.WHITE
        self.done = Style.RESET_ALL
        self.rand = random.choice([
            Fore.RED,
            Fore.GREEN,
            Fore.YELLOW,
            Fore.BLUE,
            Fore.MAGENTA,
            Fore.CYAN,
            Fore.WHITE
        ])

while True:
    cmd = input("Enter command, press help for help >> ")
    if cmd == "help":
        print('''
---------------- Help --------------------
1. Help: Show this page
2. Add: Add a task
3. Remove: Remove a task
4. List: List all tasks
5. Done: Mark a task as done
6. Undone: Mark a task as undone
7. Reset: Reset all tasks
8. Exit: Exit the program
9. Choice: Return a random choice of the tasks
        ''')
    elif cmd == "add":
        taskName = input("Enter task name: ")
        task = input("Enter task description: ")
        with open("todo.json", 'r') as f:
            data = json.load(f)
        toAppend = {
            "name": taskName,
            "description": task,
            "done": False
        }
        data["tasks"].append(toAppend)
        with open("todo.json", 'w') as f:
            json.dump(data, f, indent=4)
    elif cmd == "remove":
        taskName = input("Enter task name: ")
        with open("todo.json", 'r') as f:
            data = json.load(f)
        for task in data["tasks"]:
            if task["name"] == taskName:
                data["tasks"].remove(task)
        with open("todo.json", 'w') as f:
            json.dump(data, f, indent=4)
    elif cmd == "list":
        with open("todo.json", 'r') as f:
            data = json.load(f)
        for task in data["tasks"]:
            color = c().rand
            print(f"{color}Name: {task['name']}{c().done}")
            print(f"{color}Description: {task['description']}{c().done}")
            print(f"{color}Done: {str(task['done'])}{c().done}")
            print("-------------------------------")
    elif cmd == "done":
        taskName = input("Enter task name: ")
        with open("todo.json", 'r') as f:
            data = json.load(f)
        for task in data["tasks"]:
            if task["name"] == taskName:
                task["done"] = True
        with open("todo.json", 'w') as f:
            json.dump(data, f, indent=4)
    elif cmd == "undone":
        taskName = input("Enter task name: ")
        with open("todo.json", 'r') as f:
            data = json.load(f)
        for task in data["tasks"]:
            if task["name"] == taskName:
                task["done"] = False
        with open("todo.json", 'w') as f:
            json.dump(data, f, indent=4)
    elif cmd == "reset":
        with open("todo.json", 'w') as f:
            json.dump({
                "tasks": []
            }, f, indent=4)
    elif cmd == "choice":
        with open("todo.json", 'r') as f:
            data = json.load(f)
        notDone = []
        for task in data["tasks"]:
            if task['done'] == False:
                notDone.append(task)
        randomChoice = random.choice(notDone)
        print(f'''
I Choose:
Name: {randomChoice["name"]}
Description: {randomChoice["description"]}
        ''')
    elif cmd == "exit":
        break
    else:
        print("Invalid command")