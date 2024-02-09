# YNAB Budget Info and Balances to CSV
Python script to request budget balances from a YNAB (You Need A Budget) Account and export as a `.csv` file.

You will need a [Token key from YNAB (You Need a Budget)](https://api.ynab.com/) in order to call the API: https://api.ynab.com/v1/budgets

You will also need your Budget ID.

This code utilizes an `.env` file which you will need to create to hold the information above.

The format should look like: 

```
BASE_URL=https://api.ynab.com/v1/budgets
TOKEN=<YOUR_YNAB_TOKEN>
BUDGET_ID=<YOUR_YNAB_BUDGET_ID>
```

Before running the script, create a directory in the root of the project named `output`. This is where the files will be saved.

Run the script from the command line/terminal with

```
python get_balances.py
```

The `.csv` will be outputted to a folder named `output`. 