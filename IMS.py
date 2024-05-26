# Author: Pratham Raj Singh
# Last Modified: 2023-11-30 04:17 AM
# v0.4.7
# ===========================================================================================================

# --- Module Imports ---

import json, time, datetime, os, inquirer
from colr import color

# --- Global Vars ---

user_home_dir = os.path.expanduser("~")
folder_name = "Inventory Management System"
fileinventory = os.path.join(user_home_dir, folder_name, "inventory.json")
filetransactions = os.path.join(user_home_dir, folder_name, "transactions.txt")

if not os.path.exists(os.path.join(user_home_dir, folder_name)):
    os.makedirs(os.path.join(user_home_dir, folder_name))
    with open(fileinventory, "w") as file:
        json.dump({}, file, indent=2)
    with open(filetransactions, "w") as file:
        file.write("")

# --- Initialise ---

def Main():
    AppText("Welcome", True)
    MainMenu()

# --- Menu Management Functions ---

def MainMenu():
    qry = Menu(
        "Main Menu",
        [
            ("● Inventory", "Inventory"),
            ("● About", "About"),
            ("◄ Exit", "Exit"),
        ],
    )
    cls()
    if qry == "Inventory":
        InventoryMenu()
    elif qry == "Exit":
        ExitApp()


def InventoryMenu():
    qry = Menu(
        "Inventory Menu",
        [
            ("● View Inventory", "ViewInventory"),
            ("● Sell Item", "SellItem"),
            ("● Add Item", "AddItem"),
            ("● Update Item", "UpdateItem"),
            ("● Rename Item", "RenameItem"),
            ("● Remove Item", "RemoveItem"),
            ("◄ Back", "Back"),
        ],
    )
    cls()
    if qry == "ViewInventory":
        ViewInventory()
        InventoryMenu()
    elif qry == "SellItem":
        SellItemInventory()
        InventoryMenu()
    elif qry == "AddItem":
        AddItemInventory()
        InventoryMenu()
    elif qry == "UpdateItem":
        UpdateItemInventory()
        InventoryMenu()
    elif qry == "RenameItem":
        RenameItemInventory()
        InventoryMenu()
    elif qry == "RemoveItem":
        RemoveItemInventory()
        InventoryMenu()
    elif qry == "Back":
        MainMenu()


# --- Functions (ControlUnit) ---


def ViewInventory():
    printc("\nInventory > ", "title")
    for item, details in LoadFile(fileinventory, "json").items():
        printc(f"▪ {item}: ", fore="red", style="bright", end="")
        print(f"In Stock: {details['quantity']}, Price: {details['price']} each.")


def SellItemInventory():
    printc("\nSell Item > ", "title")
    printc("(Leave Blank to Skip)", "caption")
    item = input("Enter Item Name: ").strip().title()
    if len(item) and not (item.isnumeric()):
        inv = LoadFile(fileinventory, "json")
        if item in inv:
            while True:
                try:
                    quantity = int(input("Enter Quantity: ").strip())
                    break
                except ValueError:
                    printc("Invalid Quantity!", type="error")
            if item in inv and inv[item]["quantity"] >= quantity:
                inv[item]["quantity"] -= quantity
                RecordTransaction(item, quantity, "Sold")
                printc(f"{quantity} {item}(s) sold.", "success")
                SaveFile(fileinventory, inv, "json")
            else:
                printc(f"Not enough stock of {item}.", "error")
        else:
            printc(f"{item} not in Inventory.", "error")


def AddItemInventory():
    printc("\nAdd Item > ", "title")
    printc("(Leave Blank to Skip)", "caption")
    item = input("Enter Item Name: ").strip().title()
    if len(item) and not (item.isnumeric()):
        while True:
            try:
                quantity = int(input("Enter Quantity: ").strip())
                break
            except ValueError:
                printc("Invalid Quantity!", type="error")
        while True:
            try:
                price = float(input("Enter Price per unit: ").strip())
                break
            except ValueError:
                printc("Invalid Price!", type="error")
        inv = LoadFile(fileinventory, "json")
        if item in inv:
            inv[item]["quantity"] += quantity
        else:
            inv[item] = {
                "quantity": quantity,
                "price": price,
            }
        SaveFile(fileinventory, inv, "json")
        printc(f"{quantity} {item}(s) added to the Inventory.", "success")


def UpdateItemInventory():
    printc("\nUpdate Item > ", "title")
    printc("(Leave Blank to Skip)", "caption")
    item = input("Enter Item Name: ").strip().title()
    if len(item) and not (item.isnumeric()):
        inv = LoadFile(fileinventory, "json")
        if item in inv:
            while True:
                try:
                    new_quantity = int(input("Enter New Quantity: ").strip())
                    break
                except ValueError:
                    printc("Invalid Quantity!", "error")
            while True:
                new_price = input("Enter New Price (optional): ").strip()
                if len(new_price) != 0:
                    try:
                        new_price = float(new_price)
                        break
                    except ValueError:
                        printc("Invalid Price!", "error")
                else:
                    break
            inv[item]["quantity"] = new_quantity
            if new_price:
                inv[item]["price"] = float(new_price)
            RecordTransaction(item, new_quantity, "Updated")
            SaveFile(fileinventory, inv, "json")
            printc(f"{item} updated in Inventory.", "success")
        else:
            printc(f"{item} not in Inventory.", "error")


def RenameItemInventory():
    printc("\nRename Item > ", "title")
    printc("(Leave Blank to Skip)", "caption")
    item = input("Enter Item Old Name: ").strip().title()
    if len(item) and not (item.isnumeric()):
        inv = LoadFile(fileinventory, "json")
        if item in inv:
            while True:
                new_item = input("Enter Item New Name: ").strip().title()
                if len(new_item) and not (new_item.isnumeric()):
                    break
                else:
                    printc("Invalid Item Name!", "error")
            inv[new_item] = inv.pop(item)
            SaveFile(fileinventory, inv, "json")
            printc(f"{item} renamed to {new_item}.", "success")
        else:
            printc(f"{item} not in Inventory.", "error")


def RemoveItemInventory():
    qry = Menu(
        "Remove Item",
        [
            ("● Remove Single Item", "RemoveSingleItem"),
            ("● Remove Multiple Items", "RemoveMultipleItems"),
            ("◄ Back", "Back"),
        ],
    )
    cls()
    if qry == "RemoveSingleItem":
        printc("\nRemove Single Item > ", "title")
        printc("(Leave Blank to Skip)", "caption")
        item = input("Enter Item Name: ").strip().title()
        if len(item) and not (item.isnumeric()):
            inv = LoadFile(fileinventory, "json")
            if item in inv:
                del inv[item]
                SaveFile(fileinventory, inv, "json")
                printc(f"{item} Removed.", "success")
            else:
                printc(f"{item} not in Inventory.", "error")

    elif qry == "RemoveMultipleItems":
        printc("\nRemove Multiple Items > ", "title")
        inv = LoadFile(fileinventory, "json")
        itemlist = list(inv.keys())
        delitems = inquirer.prompt(
            [
                inquirer.Checkbox(
                    "delitems",
                    message="Select Items to Remove: (Use Left/Right Arrow Keys to Select/Deselect)",
                    choices=itemlist,
                )
            ]
        )
        for item in delitems["delitems"]:
            del inv[item]
        SaveFile(fileinventory, inv, "json")
        printc(str(len(delitems["delitems"])) + " Items Removed.", "success")
    elif qry == "Back":
        InventoryMenu()


def ExitApp():
    AppText("Exit", True)
    time.sleep(1)
    exit()


# --- Interface Funcs ---


def Menu(menutitle, choices: list):
    print()
    cursor("hide")
    qry = [inquirer.List("choice", message=menutitle, choices=choices, carousel=True)]
    return inquirer.prompt(qry)["choice"]


def AppText(TextState, animate=False):
    if TextState == "Welcome":
        TextList = [
            "*************************************",
            "*    Welcome to Inventory System    *",
            "*          Management System        *",
            "*************************************",
        ]
    elif TextState == "Exit":
        TextList = [
            "*************************************",
            "*            Developed By -         *",
            "*         Pratham Raj Singh         *",
            "*************************************",
        ]
    print()
    for i in range(len(TextList)):
        printc(TextList[i], fore="yellow", style="bright")
        if animate:
            time.sleep(0.1)


def cls():
    print("\033c", end="")
    AppText("Welcome")


def cursor(state):
    if state == "hide":
        print("\033[?25l", end="")
    elif state == "show":
        print("\033[?25h", end="")


def printc(text, type="", fore="white", back=None, style="normal", end="\n"):
    if type == "":
        stylec = color(text, fore=fore, back=back, style=style)
    elif type == "error":
        stylec = color(text + "\n", fore="red", back=back, style="bright")
    elif type == "success":
        stylec = color("\n" + text, fore="green", back=back, style="bright")
    elif type == "title":
        stylec = color(text, fore="cyan", back=back, style="bright")
    elif type == "caption":
        stylec = color(text, fore="grey", style="normal")
    print(stylec, end=end)


# --- Read / Write Funcs ---


def RecordTransaction(item, quantity, transaction_type):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    transaction = (
        f"{timestamp} - {transaction_type.capitalize()}: {quantity} {item}(s)\n"
    )
    SaveFile(filetransactions, transaction, mode="a")


def LoadFile(path, filetype="txt"):
    try:
        with open(path, "r") as file:
            if filetype == "json":
                return json.load(file)
            elif filetype == "txt":
                return file.read()
    except FileNotFoundError:
        printc(f'Unable to load: "{path}"', type="error")
        return None


def SaveFile(path, data, filetype="txt", mode="w"):
    with open(path, mode) as file:
        if filetype == "json":
            json.dump(data, file, indent=2)
        elif filetype == "txt":
            file.write(data)


if __name__ == "__main__":
    Main()