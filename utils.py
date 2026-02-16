import secrets
import hashlib

# Password hashing function (for password security)
def hash_pass(password):
    return hashlib.sha256(password.encode()).hexdigest()

def generate_account_number(existing_numbers):
    while True:
        account_number = str(secrets.randbelow(9000000000) + 1000000000)
        if account_number not in existing_numbers:
            return account_number

