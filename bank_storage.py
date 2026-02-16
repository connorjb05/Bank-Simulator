import pandas as pd
import os
from datetime import datetime

ACCOUNTS_FILE = "accounts.xlsx"
TRANSACTIONS_FILE = "transactions.xlsx"

def init_files():
    if not os.path.exists(ACCOUNTS_FILE):
        print("No storage file found for accounts! Creating one...")
        df = pd.DataFrame(columns=["account_num", "username", "password", "balance", "last_login", "date_opened"])
        df.to_excel(ACCOUNTS_FILE, index=False)
        print("Successfully created storage file for accounts!")
    
    if not os.path.exists(TRANSACTIONS_FILE):
        print("No storage file found for transactions! Creating one...")
        df = pd.DataFrame(columns=["timestamp", "account_num", "type", "amount", "balance"])
        df.to_excel(TRANSACTIONS_FILE, index=False)
        print("Successfully created storage file for transactions!")

def get_accounts_df():
    return pd.read_excel(ACCOUNTS_FILE)

def save_accounts_df(df):
    df.to_excel(ACCOUNTS_FILE, index=False)

def get_transactions_df():
    return pd.read_excel(TRANSACTIONS_FILE)

def save_transactions_df(df):
    df.to_excel(TRANSACTIONS_FILE, index=False)

