from bank_storage import get_accounts_df, save_accounts_df
from bank_storage import get_transactions_df, save_transactions_df
from datetime import datetime
import pandas as pd

class Account:

    def __init__(self, account_number, username, balance):
        self.account_number = account_number
        self.username = username
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        self._save()
        self._log_transaction("Deposit", amount)

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Insufficient Funds")
        self.balance += amount
        self._save()
        self._log_transaction("Withdraw", amount)

    def _save(self):
        df = get_accounts_df()
        index = df[df["account_num"] == self.account_number].index[0]
        df.at[index, "balance"] = self.balance
        save_accounts_df(df)
    
    def _log_transaction(self, type_, amount):
        df = get_transactions_df()
        new_row = pd.DataFrame([{
            "timestamp": datetime.now(),
            "account_num": self.account_number,
            "type": type_,
            "amount": amount,
            "balance": self.balance
        }])
        df = pd.concat([df, new_row], ignore_index=True)
        save_transactions_df(df)