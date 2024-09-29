import fire
import json
import os

# Declare the global variable to hold transactions
transactions = []

class FinanceManager:
    def __init__(self):
        self._load_transactions()

    def _load_transactions(self):
        """Load transactions from a JSON file if it exists."""
        global transactions
        if os.path.exists('transactions.json'):
            with open('transactions.json', 'r') as file:
                transactions = json.load(file)
        else:
            transactions = []

    def _save_transactions(self):
        """Save the current transactions to a JSON file."""
        global transactions
        with open('transactions.json', 'w') as file:
            json.dump(transactions, file, indent=4)

    def add_entry(self, amount, category, description, month, type='income'):
        """Add an income or expense transaction for a specific month."""
        global transactions
        transaction = {'amount': amount, 'category': category, 'description': description, 'type': type, 'month': month}
        if transaction not in transactions:
            transactions.append(transaction)
        else:
            return f"Alread data is available"
        self._save_transactions()
        return f"Added {type} transaction for {month}: {description}"

    def update_entry(self, month=None, amount=None, category=None, description=None, new_amount=None, new_category=None, new_description=None):
        """Update transactions that match the given condition (month, amount, category, or description)."""
        global transactions
        updated = False
        for transaction in transactions:
            if (month is not None and transaction['month'] == month) or \
               (amount is not None and transaction['amount'] == amount) or \
               (category is not None and transaction['category'] == category) or \
               (description is not None and transaction['description'] == description):
                if new_amount:
                    transaction['amount'] = new_amount
                if new_category:
                    transaction['category'] = new_category
                if new_description:
                    transaction['description'] = new_description
                updated = True
        
        if updated:
            self._save_transactions()
            return "Transaction(s) updated successfully."
        else:
            return "No matching transactions found."

    def delete_entry(self, month=None, amount=None, category=None, description=None):
        """Delete transactions that match the given condition (month, amount, category, or description)."""
        global transactions
        initial_len = len(transactions)
        transactions = [transaction for transaction in transactions if not (
            (month is not None and transaction['month'] == month) or
            (amount is not None and transaction['amount'] == amount) or
            (category is not None and transaction['category'] == category) or
            (description is not None and transaction['description'] == description)
        )]

        if len(transactions) < initial_len:
            self._save_transactions()
            return "Transaction(s) deleted successfully."
        else:
            return "No matching transactions found."

    def list_transactions(self, month=None,monthlyexpenses=None):
        """List all transactions, or filter by month."""
        global transactions
        if not transactions:
            return "No transactions available."
        result = []
        total_amount = 0
        for i, transaction in enumerate(transactions):
            if month is None or transaction['month'] == month:
                result.append(f"{i}: {transaction['type'].capitalize()} | Amount: {transaction['amount']} | Category: {transaction['category']} | Description: {transaction['description']} | month: {transaction['month']}")
                total_amount += transaction['amount']  # Sum up the transaction amounts
        # report = f"\nFinancial Report for {month if month else 'all months'}: Total Amount: {total_amount}"
        if monthlyexpenses is not None:
            report = f"\nFinancial Report for {month if month else 'all months'}: Total expenditure: {total_amount}"
            return  report 
        return "\n".join(result)
if __name__ == '__main__':
    fire.Fire(FinanceManager)
