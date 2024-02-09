import requests
import csv
import datetime
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Constants
BASE_URL = "https://api.ynab.com/v1"
TOKEN = os.getenv("TOKEN")  # Loaded from .env file

# Headers for authentication
headers = {
    "Authorization": f"Bearer {TOKEN}"
}

def export_to_csv(accounts_data):
    # Ensure the output directory exists
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)  # Creates the directory if it doesn't exist
    
    # Generate the filename with the current timestamp
    current_time = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"daily_balance_{current_time}.csv"
    filepath = os.path.join(output_dir, filename)  # Updated file path
    
    # Write data to the CSV file in the specified output directory
    with open(filepath, 'w', newline='') as csvfile:
        fieldnames = ['Date', 'Account_ID', 'Account', 'Balance']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for account in accounts_data:
            writer.writerow({
                'Date': datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                'Account_ID': account['id'],
                'Account': account['name'],
                'Balance': f"${account['balance'] / 1000:,.2f}"
            })

    print(f"Data exported to {filepath}")
    return filepath

def list_budgets():
    url = f"{BASE_URL}/budgets"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        budgets = response.json()['data']['budgets']
        for budget in budgets:
            print(f"Budget Name: {budget['name']}, Budget ID: {budget['id']}")
    else:
        print(f"Error listing budgets: {response.status_code}")
        print(response.text)

def get_account_balances(budget_id):
    url = f"{BASE_URL}/budgets/{budget_id}/accounts"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        accounts = response.json()['data']['accounts']
        active_accounts = [acc for acc in accounts if not acc['closed']]
        return export_to_csv(active_accounts)
    else:
        print(f"Error getting account balances: {response.status_code}")
        print(response.text)
        return None

if __name__ == "__main__":
    # Use the environment variable for the budget ID
    budget_id = os.getenv("BUDGET_ID")
    if budget_id:
        output_filename = get_account_balances(budget_id)
        if output_filename:
            print(f"CSV file generated: {output_filename}")
        else:
            print("No output generated.")
    else:
        print("BUDGET_ID environment variable not found. Please check your .env file.")
