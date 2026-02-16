from bank_storage import get_accounts_df, save_accounts_df
from utils import hash_pass, generate_account_number
from datetime import datetime
from account import Account
import pandas as pd

def register(username, password):
    df = get_accounts_df()

    if username in df["username"].values:
        return False
    
    account_number = generate_account_number(set(df["account_num"].astype(str)))

    new_row = pd.DataFrame([{
        "account_num": account_number,
        "username": username,
        "password": hash_pass(password),
        "balance": 0,
        "last_login": None,
        "date_opened": datetime.now()
    }])

    df = pd.concat([df, new_row], ignore_index=True)
    save_accounts_df(df)

    return True

def login(username, password):
    df = get_accounts_df()

    row = df[df["username"] == username]

    if row.empty:
        return None
    
    if hash_pass(password) == str(row["password"].values[0]):
        return Account(
            row["account_num"].values[0],
            username,
            row["balance"].values[0]
        )
    
    return None

