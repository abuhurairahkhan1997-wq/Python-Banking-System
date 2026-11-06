# ============================================================
#                 PYTHON NATIONAL BANK
#              COMPLETE BANKING PROJECT
# ============================================================

from itertools import islice


# ============================================================
# 1. BANK DETAILS AND CONSTANTS
# ============================================================

BANK_NAME = "Python National Bank"
IFSC_PREFIX = "PYNB"

branch_code = 101
interest_rate = 4.0
is_open = True

# Tuples - fixed values
ACCOUNT_TYPES = ("Savings", "Current", "Salary")
BRANCHES = ("London", "Manchester", "Edinburgh")

# Sets - unique values
VALID_TYPES = set(ACCOUNT_TYPES)
BLACKLIST = {"admin", "test", "fraud"}

# Minimum balance rules
MIN_BALANCE = {
    "Savings": 1000,
    "Current": 5000,
    "Salary": 0
}

# Maximum withdrawal amount
WITHDRAW_LIMIT = 50000

# Main banking database
accounts = {}

# Store unique account numbers
used_numbers = set()


# ============================================================
# 2. BASIC FUNCTIONS
# ============================================================

def banner(title, width=50):
    """Display a formatted heading."""
    print("\n" + "=" * width)
    print(title.center(width))
    print("=" * width)


def format_money(amount):
    """Format an amount as money."""
    return f"${amount:,.2f}"


def clean_name(name):
    """Remove extra spaces and convert name to title case."""
    return name.strip().title()


def validate_pin(pin):
    """PIN must contain exactly four digits."""
    pin = str(pin).strip()
    return pin.isdigit() and len(pin) == 4


def check_tier(balance):
    """Return customer tier according to account balance."""

    if balance >= 100000:
        return "Platinum"

    elif balance >= 50000:
        return "Gold"

    elif balance >= 10000:
        return "Silver"

    else:
        return "Basic"


# ============================================================
# 3. GENERATE UNIQUE ACCOUNT NUMBER
# ============================================================

def generate_account_number(used_numbers):

    serial = len(used_numbers) + 1

    account_number = f"{IFSC_PREFIX}{serial:04d}"

    while account_number in used_numbers:

        serial += 1

        account_number = f"{IFSC_PREFIX}{serial:04d}"

    used_numbers.add(account_number)

    return account_number


# ============================================================
# 4. *ARGS AND LAMBDA FUNCTIONS
# ============================================================

def total_of(*amounts):
    """Add any number of amounts."""
    return sum(amounts)


# Simple Interest
simple_interest = lambda principal, rate, years: (
    principal * rate * years / 100
)


# Transfer fee
transfer_fee = lambda amount: (
    0
    if amount <= 10000
    else round(amount * 0.005, 2)
)


# Rich customer check
is_rich = lambda balance: balance >= 50000


# ============================================================
# 5. CUSTOM EXCEPTIONS
# ============================================================

class BankError(Exception):
    """Base class for banking errors."""
    pass


class InsufficientFundsError(BankError):
    pass


class InvalidAmountError(BankError):
    pass


class AccountNotFoundError(BankError):
    pass


class AuthenticationError(BankError):
    pass


# ============================================================
# 6. ACCOUNT AND INPUT VALIDATION
# ============================================================

def get_account(acc_no):
    """Find and return an account."""

    acc_no = str(acc_no).strip().upper()

    if acc_no not in accounts:

        raise AccountNotFoundError(
            f"Account {acc_no} not found."
        )

    return accounts[acc_no]


def validate_amount(value):
    """Check that amount is numeric and greater than zero."""

    try:

        amount = float(value)

    except (ValueError, TypeError):

        raise InvalidAmountError(
            "Amount must be a number."
        )

    if amount <= 0:

        raise InvalidAmountError(
            "Amount must be greater than zero."
        )

    return round(amount, 2)


def verify_pin(account, pin):
    """Verify customer PIN."""

    if account["pin"] != str(pin).strip():

        raise AuthenticationError(
            "Incorrect PIN."
        )


# ============================================================
# 7. CREATE ACCOUNT
# ============================================================

def create_account(name, acc_type, opening, pin):

    # Clean customer name
    name = clean_name(name)

    # Validate name
    if len(name) < 3 or not name.replace(" ", "").isalpha():

        raise ValueError(
            "Name must contain only letters and spaces "
            "(minimum 3 characters)."
        )

    # Check blacklist
    if set(name.lower().split()) & BLACKLIST:

        raise ValueError(
            "This name is not allowed."
        )

    # Format account type
    acc_type = acc_type.strip().title()

    # Validate account type
    if acc_type not in VALID_TYPES:

        raise ValueError(
            "Account type must be one of: "
            + ", ".join(ACCOUNT_TYPES)
        )

    # Validate PIN
    pin = str(pin).strip()

    if not validate_pin(pin):

        raise ValueError(
            "PIN must be exactly 4 digits."
        )

    # Validate opening balance
    opening = validate_amount(opening)

    # Check minimum balance
    if opening < MIN_BALANCE[acc_type]:

        raise InvalidAmountError(
            f"{acc_type} account requires a minimum balance of "
            f"{format_money(MIN_BALANCE[acc_type])}."
        )

    # Generate account number
    acc_no = generate_account_number(
        used_numbers
    )

    # Store account information
    accounts[acc_no] = {

        "name": name,

        "type": acc_type,

        "pin": pin,

        "balance": opening,

        "history": [
            (
                "Opening",
                opening,
                opening
            )
        ]
    }

    return acc_no


# ============================================================
# 8. DEPOSIT
# ============================================================

def deposit(acc_no, amount):

    account = get_account(acc_no)

    amount = validate_amount(amount)

    # Add amount
    account["balance"] += amount

    # Add transaction to history
    account["history"].append(
        (
            "Deposit",
            amount,
            account["balance"]
        )
    )

    return account["balance"]


# ============================================================
# 9. WITHDRAW
# ============================================================

def withdraw(acc_no, pin, amount):

    account = get_account(acc_no)

    # Check PIN
    verify_pin(account, pin)

    amount = validate_amount(amount)

    # Check withdrawal limit
    if amount > WITHDRAW_LIMIT:

        raise InvalidAmountError(
            f"Daily withdrawal limit is "
            f"{format_money(WITHDRAW_LIMIT)}."
        )

    # Check minimum account balance
    if (
        account["balance"] - amount
        < MIN_BALANCE[account["type"]]
    ):

        raise InsufficientFundsError(
            f"Insufficient funds. "
            f"{account['type']} accounts must maintain "
            f"{format_money(MIN_BALANCE[account['type']])}."
        )

    # Deduct amount
    account["balance"] -= amount

    # Save transaction
    account["history"].append(
        (
            "Withdraw",
            amount,
            account["balance"]
        )
    )

    return account["balance"]


# ============================================================
# 10. TRANSFER MONEY
# ============================================================

def transfer(from_no, pin, to_no, amount):

    source_account = get_account(from_no)

    destination_account = get_account(to_no)

    # Prevent transfer to same account
    if source_account is destination_account:

        raise InvalidAmountError(
            "Cannot transfer money to the same account."
        )

    # Verify source PIN
    verify_pin(source_account, pin)

    amount = validate_amount(amount)

    # Calculate transfer fee
    fee = transfer_fee(amount)

    total_amount = amount + fee

    # Check available balance
    if (
        source_account["balance"] - total_amount
        < MIN_BALANCE[source_account["type"]]
    ):

        raise InsufficientFundsError(
            "Insufficient funds for transfer "
            "(amount + transfer fee)."
        )

    # Deduct money from sender
    source_account["balance"] -= total_amount

    source_account["history"].append(
        (
            "Transfer Out",
            total_amount,
            source_account["balance"]
        )
    )

    # Add money to receiver
    destination_account["balance"] += amount

    destination_account["history"].append(
        (
            "Transfer In",
            amount,
            destination_account["balance"]
        )
    )

    return fee


# ============================================================
# 11. APPLY SAVINGS INTEREST
# ============================================================

def apply_interest(rate=4.0, years=1):

    credited = {}

    for acc_no, account in accounts.items():

        if account["type"] == "Savings":

            interest = round(
                simple_interest(
                    account["balance"],
                    rate,
                    years
                ),
                2
            )

            account["balance"] += interest

            account["history"].append(
                (
                    "Interest",
                    interest,
                    account["balance"]
                )
            )

            credited[acc_no] = interest

    return credited


# ============================================================
# 12. PRINT BANK STATEMENT
# ============================================================

def print_statement(acc_no, last_n=None):

    acc_no = str(acc_no).strip().upper()

    account = get_account(acc_no)

    # All transactions or only last N transactions
    if last_n is None:

        rows = account["history"]

    else:

        rows = list(
            islice(
                reversed(account["history"]),
                last_n
            )
        )[::-1]

    banner(
        f"STATEMENT - {acc_no}"
    )

    print(
        f"Name: {account['name']} | "
        f"Type: {account['type']}"
    )

    print(
        f"{'#':<4}"
        f"{'Type':<16}"
        f"{'Amount':>14}"
        f"{'Balance':>16}"
    )

    print("-" * 52)

    for number, (
        transaction_type,
        amount,
        balance
    ) in enumerate(
        rows,
        start=1
    ):

        print(
            f"{number:<4}"
            f"{transaction_type:<16}"
            f"{amount:>14,.2f}"
            f"{balance:>16,.2f}"
        )

    print("-" * 52)

    print(
        "Closing balance:",
        format_money(
            account["balance"]
        )
    )


# ============================================================
# 13. BANK REPORT
# ============================================================

def bank_report():

    banner(
        "BANK REPORT"
    )

    if not accounts:

        print(
            "No customer accounts available."
        )

        return

    # Total deposits using generator
    total = sum(
        account["balance"]
        for account in accounts.values()
    )

    # Count accounts by type using dictionary comprehension
    count_by_type = {

        account_type: sum(
            1
            for account in accounts.values()
            if account["type"] == account_type
        )

        for account_type in ACCOUNT_TYPES
    }

    # Richest customer using max() and lambda
    richest_no, richest = max(

        accounts.items(),

        key=lambda item:
        item[1]["balance"]
    )

    print(
        f"Total customers : "
        f"{len(accounts)}"
    )

    print(
        f"Total deposits  : "
        f"{format_money(total)}"
    )

    print(
        f"Accounts by type: "
        f"{count_by_type}"
    )

    print(
        f"Richest customer: "
        f"{richest['name']} "
        f"({format_money(richest['balance'])})"
    )

    print()

    print(
        f"{'Rank':<6}"
        f"{'Acc No':<12}"
        f"{'Name':<20}"
        f"{'Tier':<12}"
        f"{'Balance':>14}"
    )

    print("-" * 64)

    # Sort accounts from highest to lowest balance
    ranking = sorted(

        accounts.items(),

        key=lambda item:
        item[1]["balance"],

        reverse=True
    )

    for rank, (
        acc_no,
        account
    ) in enumerate(
        ranking,
        start=1
    ):

        print(
            f"{rank:<6}"
            f"{acc_no:<12}"
            f"{account['name']:<20}"
            f"{check_tier(account['balance']):<12}"
            f"{account['balance']:>14,.2f}"
        )


# ============================================================
# 14. DEMONSTRATION CUSTOMERS
# ============================================================

def load_demo_customers():

    demo_customers = [

        (
            "Rohan Sharma",
            "Savings",
            75000,
            "1234"
        ),

        (
            "Simran Kaur",
            "Current",
            120000,
            "2222"
        ),

        (
            "Aman Verma",
            "Salary",
            15000,
            "3333"
        ),

        (
            "Neha Gupta",
            "Savings",
            5000,
            "4444"
        ),

        (
            "Karan Singh",
            "Current",
            48000,
            "5555"
        )
    ]

    for (
        name,
        account_type,
        balance,
        pin
    ) in demo_customers:

        create_account(
            name,
            account_type,
            balance,
            pin
        )


# ============================================================
# 15. DISPLAY MENU
# ============================================================

def print_menu():

    banner(
        "🏦 " + BANK_NAME
    )

    menu = [

        "Create Account",

        "Deposit",

        "Withdraw",

        "Transfer",

        "Check Balance",

        "Mini Statement",

        "Apply Savings Interest",

        "Bank Report"
    ]

    for number, option in enumerate(
        menu,
        start=1
    ):

        print(
            f"  {number}. {option}"
        )

    print(
        "  0. Exit"
    )


# ============================================================
# 16. MAIN BANKING PROGRAM
# ============================================================

def main():

    while True:

        print_menu()

        choice = input(
            "\nEnter choice: "
        ).strip()

        try:

            # =================================================
            # OPTION 1 - CREATE ACCOUNT
            # =================================================

            if choice == "1":

                name = input(
                    "Customer name   : "
                )

                acc_type = input(
                    f"Type {ACCOUNT_TYPES}: "
                )

                opening = input(
                    "Opening deposit : "
                )

                pin = input(
                    "Set 4-digit PIN : "
                )

                acc_no = create_account(
                    name,
                    acc_type,
                    opening,
                    pin
                )

                print(
                    f"✅ Account created successfully!"
                )

                print(
                    f"Your account number is {acc_no}"
                )


            # =================================================
            # OPTION 2 - DEPOSIT
            # =================================================

            elif choice == "2":

                acc_no = input(
                    "Account number : "
                )

                amount = input(
                    "Amount         : "
                )

                balance = deposit(
                    acc_no,
                    amount
                )

                print(
                    "✅ Deposit successful."
                )

                print(
                    "Balance:",
                    format_money(balance)
                )


            # =================================================
            # OPTION 3 - WITHDRAW
            # =================================================

            elif choice == "3":

                acc_no = input(
                    "Account number : "
                )

                pin = input(
                    "PIN            : "
                )

                amount = input(
                    "Amount         : "
                )

                balance = withdraw(
                    acc_no,
                    pin,
                    amount
                )

                print(
                    "✅ Please collect your cash."
                )

                print(
                    "Balance:",
                    format_money(balance)
                )


            # =================================================
            # OPTION 4 - TRANSFER
            # =================================================

            elif choice == "4":

                source = input(
                    "From account   : "
                )

                pin = input(
                    "PIN            : "
                )

                destination = input(
                    "To account     : "
                )

                amount = input(
                    "Amount         : "
                )

                fee = transfer(
                    source,
                    pin,
                    destination,
                    amount
                )

                print(
                    "✅ Transfer successful."
                )

                print(
                    "Fee charged:",
                    format_money(fee)
                )


            # =================================================
            # OPTION 5 - CHECK BALANCE
            # =================================================

            elif choice == "5":

                account = get_account(
                    input(
                        "Account number : "
                    )
                )

                verify_pin(
                    account,
                    input(
                        "PIN            : "
                    )
                )

                print(
                    f"💰 {account['name']} | "
                    f"{check_tier(account['balance'])} tier | "
                    f"{format_money(account['balance'])}"
                )


            # =================================================
            # OPTION 6 - MINI STATEMENT
            # =================================================

            elif choice == "6":

                acc_no = input(
                    "Account number : "
                )

                account = get_account(
                    acc_no
                )

                verify_pin(
                    account,
                    input(
                        "PIN            : "
                    )
                )

                print_statement(
                    acc_no,
                    last_n=5
                )


            # =================================================
            # OPTION 7 - SAVINGS INTEREST
            # =================================================

            elif choice == "7":

                credited = apply_interest(
                    rate=interest_rate
                )

                if credited:

                    for (
                        acc_no,
                        interest
                    ) in credited.items():

                        print(
                            f"✅ {acc_no} "
                            f"({accounts[acc_no]['name']}): "
                            f"interest credited "
                            f"{format_money(interest)}"
                        )

                    print(
                        "Total interest paid:",
                        format_money(
                            total_of(*credited.values())
                        )
                    )

                else:

                    print(
                        "No Savings accounts found."
                    )


            # =================================================
            # OPTION 8 - BANK REPORT
            # =================================================

            elif choice == "8":

                bank_report()


            # =================================================
            # OPTION 0 - EXIT
            # =================================================

            elif choice == "0":

                print(
                    f"\nThank you for banking with "
                    f"{BANK_NAME}. Goodbye! 👋"
                )

                break


            # =================================================
            # INVALID MENU CHOICE
            # =================================================

            else:

                print(
                    "❌ Invalid choice. Please enter "
                    "a number from 0 to 8."
                )


        # =====================================================
        # ERROR HANDLING - program never crashes
        # =====================================================

        except BankError as error:

            # Catches all custom bank errors:
            # InsufficientFundsError, InvalidAmountError,
            # AccountNotFoundError, AuthenticationError
            print(
                f"❌ {type(error).__name__}: {error}"
            )

        except ValueError as error:

            # Catches name, account type and PIN errors
            print(
                f"❌ Input error: {error}"
            )


# ============================================================
# 17. START THE PROGRAM
# ============================================================

if __name__ == "__main__":

    # Load demo customers only once
    # (stops duplicates if this cell is run again)
    if not accounts:

        load_demo_customers()

    print(
        f"{len(accounts)} demo customers loaded: "
        f"{', '.join(accounts)}"
    )

    main()
