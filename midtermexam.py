# Dictionary to store game library with their quantities and rental costs
game_library = {
    "Donkey Kong": {"quantity": 3, "cost": 2.0},
    "Super Mario Bros": {"quantity": 5, "cost": 3.0},
    "Tetris": {"quantity": 2, "cost": 1.0},
    # Add more games as needed
}

# Dictionary to store user accounts with their balances and points
user_accounts = {}

# Admin account details
admin_username = "admin"
admin_password = "adminpass"

# Function to display available games with their numbers and rental costs
def display_available_games():
    print("\nAVAILABLE GAMES")
    for item_name, item_details in game_library.items():
        cost = item_details["cost"]
        quantity = item_details["quantity"]
        print(f"Item: {item_name}, Quantity: {quantity}, Cost: {cost}")
    

# Function to register a new user
def register_user():
    print("\nREGISTER USER")

    while True:
        username = input("Enter username: ")

        if username in user_accounts:
            print("Username already exists.")
            continue

        break

    password = input("Enter password: ")
    
    user_accounts[username] = {
        "password": password,
        "balance": 0.0,
        "points": 0,
        "inventory": [],
        "spent": 0.0
    }

    print("To rent games, you would need to top-up.")

    top_up_account(username)

    return
 
# Function to rent a game
def rent_game(username):
    print("\nRENT GAME")
    while True:
        display_available_games()
        game = input("What game would you like to rent? (enter to return) ")

        if not game: return

        if game not in game_library:
            print("Game does not exist.")
            continue

        if game_library[game]["quantity"] <= 0:
            print("Game is out of stock.")
            continue
            
        if game_library[game]["cost"] > user_accounts[username]["balance"]:
            print("User does not have enough money to rent game")
            continue

        break

    game_library[game]["quantity"] -= 1
    user_accounts[username]["balance"] -= game_library[game]["cost"]
    user_accounts[username]["spent"] += game_library[game]["cost"]
    user_accounts[username]["inventory"].append(game)

    print(f"GAME RENTED: {game}")
    if user_accounts[username]["spent"] >= 2:
        points = user_accounts[username]["spent"] // 2
        user_accounts[username]["spent"] = user_accounts[username]["spent"] / 2 - user_accounts[username]["spent"] // 2
        user_accounts[username]["points"] += points
        print(f"\nUSER POINTS: {user_accounts[username]['points']}")
    print(f"USER BALANCE: {user_accounts[username]['balance']}")

    return

# Function to return a game
def return_game(username):
    print("\nRETURN GAME")
    while True:
        display_game_inventory(username)
        game = input("What game would you like to return? (enter to return) ")

        if not game: return

        if game not in user_accounts[username]["inventory"]:
            print("Game does not exist.")
            continue

        break   

    game_library[game]["quantity"] += 1
    user_accounts[username]["inventory"].remove(game)

    print(f"GAME RETURNED: {game}")
    display_game_inventory(username)


    return

# Function to top-up user account
def top_up_account(username):
    print("\nTOP-UP")
    while True: 
        try:
            amount = float(input("How much would you like to top-up? "))
            if amount <= 0:
                raise Exception()
            break
        except:
            print("Enter a valid amount.")

    user_accounts[username]["balance"] += amount
    print(f"USER BALANCE: {user_accounts[username]['balance']}")
    
    return

# Function to display user's inventory
def display_inventory(username):
    print("\nINVENTORY")

    print(f"Balance: {user_accounts[username]['balance']}")
    print(f"Points: {user_accounts[username]['points']}")
    display_game_inventory(username)

    return


# Function for admin to update game details
def admin_update_game():
    print("\nUPDATE GAME MENU")
    
    while True:
        display_available_games()
        game = input("Which game would you like to update? (enter to return) ")

        if not game: return

        if game not in game_library:
            print("Game does not exist.")
            continue
        
        try:
            game_prop = input("Detail to update (Q for Quantity, C for Cost): ").lower()
        except: 
            continue

        match game_prop:
            case "q":
                quantity = int(input(f"Change game quanity from {game_library[game]['quantity']} to: "))
                game_library[game]["quantity"] = quantity
                break
            case "c":
                cost = float(input(f"Change game quanity from {game_library[game]['cost']} to: "))
                game_library[game]["cost"] = cost
                break
            case _:
                print("Type an option.")
                continue
        
    display_available_games()

    return

# Function for admin login
def admin_login():
    print("\nADMIN LOGIN")
    
    username = input("Enter username: ")
    password = input("Enter password: ")

    if check_credentials(username, password, True):
        admin_menu()
        return
    else:
        print("Returning to menu.")
        return

# Admin menu
def admin_menu():
    options = ["UPDATE GAME DETAILS", "LOGOUT"]

    while True:
        print("\nADMIN MENU")
        for o in range(len(options)):
            print(f"{o+1}: {options[o]}")

        try:
            chosen_option = int(input("Option: "))
        except:
            continue

        match chosen_option:
            case 1:
                admin_update_game()
            case 2:
                print("Logging out...")
                break
            case _:
                print("Option not found.")
                continue
    
    return

# Function for users to redeem points for a free game rental
def redeem_free_rental(username):
    print("\nREDEEM FREE RENTAL (at least 3 points to redeem a game)")

    NEEDED_POINTS_TO_REDEEM = 3

    while True:
        display_available_games()
        game = input("What game would you like to rent using points? (enter to return) ")

        if not game: return

        if game not in game_library:
            print("Game does not exist.")
            continue
        
        if user_accounts[username]["points"] < NEEDED_POINTS_TO_REDEEM:
            print("User does not have enough points to rent game.")
            continue

        break

    game_library[game]["quantity"] -= 1
    user_accounts[username]["points"] -= NEEDED_POINTS_TO_REDEEM
    user_accounts[username]["inventory"].append(game)

    print(f"GAME RENTED using POINTS: {game}")
    print(f"USER POINTS: {user_accounts[username]['points']}")

    return

# Function to display game inventory
def display_game_inventory(username):
    print("\nGAME INVENTORY")

    print("Inventory contains: ")
    for i in user_accounts[username]['inventory']:
        print(f"> {i}")

    return

# Function to handle user's logged-in menu
def logged_in_menu(username):
    options = ["TOP-UP", "AVAILABLE GAMES", "RENT A GAME", "USE POINTS TO RENT A GAME", "RETURN GAME", "CHECK PROFILE", "LOGOUT"]

    while True:
        print("\nUSER MENU")
        for o in range(len(options)):
            print(f"{o+1}: {options[o]}")
        
        try: 
            chosen_option = int(input("Option: "))
        except:
            continue

        match chosen_option:
            case 1:
                top_up_account(username)
            case 2:
                display_available_games()
            case 3:
                rent_game(username)
            case 4:
                redeem_free_rental(username)
            case 5:
                return_game(username)
            case 6:
                display_inventory(username)
            case 7:
                print("Logging out...")
                break
            case _:
                print("Option not found.")
                continue
    
    return

# Function to handle login
def login():
    print("\nUSER LOGIN")
    
    username = input("Enter username: ")
    password = input("Enter password: ")

    if check_credentials(username, password, False):
        logged_in_menu(username)
        return
    else:
        print("Returning to menu.")
        return


# Function to check user credentials
def check_credentials(username, password, admin):
    if admin:
        if username == admin_username and password == admin_password:
            print("Admin logged in.")
            return True
        else: 
            print("Incorrect credentials.")
            return False
    
    if not admin:
        if username in user_accounts:
            if user_accounts[username]["password"] == password:
                print("Logged in.")
                return True
            else:
                print("Incorrect credentials")
                return False
        else:
            print("\nUsername does not exist.")
            return False

            
        
    
# Main function to run the program
def main():
    options = ["AVAILABLE GAMES", "LOGIN", "REGISTER", "ADMIN LOGIN", "EXIT"]

    while True:
        print("\nVIDEO GAME RENTAL SYSTEM")
        for o in range(len(options)):
            print(f"{o+1}: {options[o]}")
        print()

        try:    
            chosen_option = int(input("Option: "))
        except:
            continue

        match chosen_option:
            case 1:
                display_available_games()
            case 2:
                login()
            case 3:
                register_user()
            case 4:
                admin_login()
            case 5:
                print("EXITING...")
                break
            case _:
                print("Option not found.")
                continue



if __name__ == "__main__":
    main()
