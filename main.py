import pandas as pd
import os
import hashlib
import secrets
from datetime import datetime

ACCOUNTS_FILE = "accounts.xlsx"
TRANSACTIONS_FILE = "transactions.xlsx"

# todo hashmap that will limit login attempts and lock accounts
login_attempts = {}

# Make sure there is a file for holding accounts and their data
if not os.path.exists(ACCOUNTS_FILE):
    df = pd.DataFrame(columns=["account_num", "username", "password", "balance", "last_login", "date_opened"])
    df.to_excel(ACCOUNTS_FILE, index=False)

# Make sure theres a file for holding transactions
if not os.path.exists(TRANSACTIONS_FILE):
    df = pd.DataFrame(columns=["timestamp", "account_num", "type", "amount", "balance"])
    df.to_excel(TRANSACTIONS_FILE, index=False)

# Password hashing function (for password security)
def hash_pass(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Returns the lifetime of the account
def account_lifetime(account_number):

    df = pd.read_excel(ACCOUNTS_FILE)

    if account_number not in df["account_num"].values:
        return False
    
    now = datetime.now()
    time_opened = df["date_opened"]

    delta = time_opened - now
    
    return delta.days

# Account number generator
def generate_account_number():

    df = pd.read_excel(ACCOUNTS_FILE)

    existing_numbers = set(df["account_num"].astype(str))

    while True:
        account_number = str(secrets.randbelow(9000000000) + 1000000000)

        if account_number not in existing_numbers:
            return account_number

# Add a new user to our bank
def register(username, password):
    
    df = pd.read_excel(ACCOUNTS_FILE)
    
    if username in df["username"].values:
        return False
    
    new_row = pd.DataFrame([{
        "account_num":generate_account_number,
        "username":username,
        "password":hash_pass(password),
        "balance":0,
        "last_login":None,
        "date_opened":datetime.now()
    }])

    df = pd.concat([df, new_row], ignore_index=True)
    
    df.to_excel(ACCOUNTS_FILE, index=False)
    return True

# Verify and log the user into their banking account
def login(username, password):

    df = pd.read_excel(ACCOUNTS_FILE)

    row = df[df["username"] == username]
    
    if row.empty:
        return False
    
    # Todo login attempts limiter
    if hash_pass(password) == str(row["password"].values[0]):
        return True
    
    return False

# Updates the users accounts balance
def update_balance(account_number, amount):

    df = pd.read_excel(ACCOUNTS_FILE)

    index = df[df["account_num"] == account_number].index[0]
    
    df.at[index, "balance"] += amount
    df.to_excel(ACCOUNTS_FILE, index=False)
    log_transaction(account_number, 
                    "Deposit" if amount > 0 else "Withdraw", 
                    abs(amount), 
                    df.at[index, "balance"])

# Logs the latest transaction of an account
def log_transaction(account_number, transaction_type, amount, balance_after):

    df = pd.read_excel(TRANSACTIONS_FILE)

    new_row = pd.DataFrame([{
        "timestamp":datetime.now(),
        "account_num":account_number,
        "type":transaction_type,
        "amount":amount,
        "balance":balance_after
    }])

    df = pd.concat([df, new_row], 
                   ignore_index=False)
    df.to_excel(TRANSACTIONS_FILE, index=False)

def main():

    print("\nWelcome To")
    print("BENNY'S BANK:")

    while True:
        print("\nOptions:")
        print("'login' to log into your account")
        print("'register' to create an account\n")
        option = input("Select an option: ").casefold()

        if option == "login":
            while True:

                username = input("Username: ").casefold()
                if username == "quit":
                    break

                password = input("Password: ").casefold()
                if password == "quit":
                    break

                if not login(username, password):
                    print("Could not authenticate given information. Please try again")
                    continue
                else:
                    print("\nYou successfully logged into your account.\n")

                    print(username + "'s Account:\nType 'logout' to logout of this account.\n")
                    print("Balance: $TODO\n")
                    input() # todo handle this

        elif option == "register":
            while True:

                username = input("Username: ")
                if username.casefold() == "quit":
                    break

                password = input("Password: ")
                if password.casefold() == "quit":
                    break

                if not register(username, password):
                    print("Registration failed. Please try again")
                    continue
                else:
                    print("\nYou have successfully registered a new bank account.")
                    break

        else:
            print("Incorrect option. please try again.")
            continue
    return

main()