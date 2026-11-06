# Python National Bank: Banking System Simulation

A menu-driven banking program in core Python. You can open accounts, deposit, withdraw, transfer money with fees, check balances and customer tiers, print mini statements, pay savings interest and run a bank-wide report. Custom exceptions stop bad input from crashing the program.

> Project from my Python module on the Skill Versed Post Graduation in Data Analytics with Gen AI (batch PGDA0526).

## Features
| Option | What it does |
|---|---|
| 1. Create account | Savings, Current or Salary; checks the name, PIN and minimum opening balance |
| 2. Deposit | Adds money and logs it in the account history |
| 3. Withdraw | Needs the PIN; enforces a 50,000 limit per withdrawal and the minimum balance |
| 4. Transfer | Free up to 10,000, then a 0.5% fee; blocks transfers to the same account |
| 5. Check balance | Shows the balance and customer tier (Platinum, Gold, Silver or Basic) |
| 6. Mini statement | The last 5 transactions in a lined-up table |
| 7. Savings interest | 4% simple interest, paid to Savings accounts only |
| 8. Bank report | Total deposits, accounts by type, richest customer and a balance ranking |

Five demo customers load at start-up, so you can test straight away.

## Python concepts used
- **Data structures:** dictionaries (the accounts database), tuples (fixed account types; history records), sets (unique account numbers, blacklist checks with `&`), lists
- **Functions:** default arguments, `*args`, and **lambda** functions for interest and fee rules
- **Custom exceptions:** `InsufficientFundsError`, `InvalidAmountError`, `AccountNotFoundError` and `AuthenticationError`, all inheriting from `BankError`, so one `except` catches them all
- **Error handling:** `try-except` around every menu action
- **Comprehensions and generators:** a dictionary comprehension counts accounts by type, and a generator inside `sum()` totals deposits
- **Built-ins:** `max()` and `sorted()` with lambda keys, `enumerate()`, `reversed()` with `itertools.islice()`
- **f-string formatting:** money (`$1,500.00`), zero-padded account numbers (`PYNB0001`) and aligned columns

## Example
```
Enter choice: 4
From account   : PYNB0002
PIN            : 2222
To account     : PYNB0003
Amount         : 20000
✅ Transfer successful.
Fee charged: $100.00

Enter choice: 3
Account number : PYNB0001
PIN            : 0000
Amount         : 100
❌ AuthenticationError: Incorrect PIN.
```
A full session running all 18 tests is in [`docs/sample_run.txt`](docs/sample_run.txt).

## Testing
All 18 tests in the notebook's checklist passed. They cover creating accounts, rejecting bad names, PINs and account types, minimum balances, text typed as an amount, wrong PINs, the withdrawal limit, transfers with and without fees, same-account transfers, statements, interest, the bank report and invalid menu choices.

## How to run
**Google Colab:** open `Python_National_Bank.ipynb` and choose **Runtime → Run all**. The last cell starts the menu.

**On your computer (Python 3):**
```
python python_national_bank.py
```

Demo logins: `PYNB0001` / PIN `1234`, `PYNB0002` / `2222`, `PYNB0003` / `3333`, `PYNB0004` / `4444`, `PYNB0005` / `5555`.

## Files
| File | What it is |
|---|---|
| `Python_National_Bank.ipynb` | Notebook with explanations for each section |
| `python_national_bank.py` | The same code as a single script |
| `docs/sample_run.txt` | Output from running all 18 tests |

## Author
**Abuhurairah Rahman Pathan**, MSc Bioinformatics, University of Liverpool
[LinkedIn](https://www.linkedin.com/in/pathan-abuhurairah-rahman-1997-khan)
