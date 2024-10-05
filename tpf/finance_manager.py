import fire
from database import users_collection, db
from pymongo.errors import PyMongoError
from datetime import datetime
from bson import ObjectId

class FinanceManager:
    def __init__(self):
        self.db = db
        self.transactions_collection = users_collection  # Users collection where we store user data

    def expenses_add_update(self, username, amount, category, month=None, year=None, day=None,Budget=3000):
        user = users_collection.find_one({"username": username})
        if not user:
            return "User not found."
        user_id = user['_id']
        if month is None:
            month = datetime.now().strftime("%B")
        if year is None:
            year = datetime.now().year
        if day is None:
            day = datetime.now().day
        transaction = {
            'amount': amount,
            'category': category,
            'month': month,
            'year': year,
            'day': day
        }
        try:
            income_data = user.get('incomefield', [])
            income_sandy=0
            if income_data:
                for income in income_data:
                    if income['month'] == month:
                        if income['year']== year:
                            income_sandy=income['income']
            else:
                print("No income data found.")
            if income_sandy>0:
                Budget= int(income_sandy * (50 / 100))
                total_expenses = 0
                if "transactions" in user and isinstance(user["transactions"], list):
                    for trans in user["transactions"]:
                        if trans["month"] == month and trans["year"] == year:
                            total_expenses += trans["amount"]
                if total_expenses + amount > Budget:
                    return f"Cannot add expense. Budget exceeded! Current total: {total_expenses}, Budget: {Budget}, New Expense: {amount}"

                if not isinstance(user.get("transactions", []), list):
                    users_collection.update_one(
                        {"_id": user_id},
                        {"$set": {"transactions": []}}
                    )
                existing_transaction = users_collection.find_one({
                    "_id": user_id,
                    "transactions": {
                        "$elemMatch": {
                            "category": category,
                            "month": month,
                            "year": year,
                            "day": day
                        }
                    }
                })
                if existing_transaction:
                    users_collection.update_one(
                        {"_id": user_id, "transactions.month": month, "transactions.year": year, "transactions.day": day},
                        {"$set": {"transactions.$": transaction}}
                    )
                    return f"Updated transaction for {username} successfully for {month} {year} on day {day}."
                else:
                    users_collection.update_one(
                        {"_id": user_id},
                        {"$push": {"transactions": transaction}}
                    )
                    return f"Added transaction for {username} successfully for {month} {year} on day {day}."
            else:
                return f"you dont have income to buy something"
        except PyMongoError as e:
            return f"An error occurred: {str(e)}"

    def expenses_read(self, username=None, month=None, year=None, day=None):
        now = datetime.now()
        month = month or now.strftime("%B")
        year = year or now.year
        day = day or now.day
        query = {}
        if username:
            user = users_collection.find_one({"username": username})
            if not user:
                return "User not found."
            query['_id'] = user['_id']
        transactions_query = {}
        if month:
            transactions_query["month"] = month
        if year:
            transactions_query["year"] = year
        if day:
            transactions_query["day"] = day
        query["transactions"] = {"$elemMatch": transactions_query}
        user_transactions = users_collection.find_one(query)
        if user_transactions and "transactions" in user_transactions:
            matched_transactions = [
                transaction for transaction in user_transactions["transactions"]
                if (transaction["month"] == month and
                    transaction["year"] == year and
                    (transaction["day"] == day))
            ]
            if matched_transactions:
                return matched_transactions
        else:
            return "No transactions found for the user."

    def income_add_update(self, username, income, month=None, year=None):
        user = users_collection.find_one({"username": username})
        if not user:
            return "User not found."
        user_id = user['_id']
        if month is None:
            month = datetime.now().strftime("%B")
        if year is None:
            year = datetime.now().year
        incomefield = {
            'income': income,
            'month': month,
            'year': year,
        }
        try:
            if not isinstance(user.get("incomefield", []), list):
                users_collection.update_one(
                    {"_id": user_id},
                    {"$set": {"incomefield": []}}
                )
            existing_transaction = users_collection.find_one({
                "_id": user_id,
                "incomefield": {
                    "$elemMatch": {
                        "month": month,
                        "year": year,
                    }
                }
            })
            print(existing_transaction)
            if existing_transaction:
                users_collection.update_one(
                    {"_id": user_id, "incomefield.month": month, "incomefield.year": year},
                    {"$set": {"incomefield.$": incomefield}}
                )
                return f"Updated income for {username} successfully for {month} {year}."
            else:
                users_collection.update_one(
                    {"_id": user_id},
                    {"$push": {"incomefield": incomefield}}
                )
                return f"Added income for {username} successfully for {month} {year}"
        except PyMongoError as e:
            return f"An error occurred: {str(e)}"
    def income_read(self, username=None, month=None, year=None):
        user = users_collection.find_one({"username": username})
        now = datetime.now()
        month = month or now.strftime("%B")
        year = year or now.year
        income_data = user.get('incomefield', [])
        # print(income_data)
        if income_data:
            for income in income_data:
                # print(income['month'])
                if income['month'] == month:
                    if income['year']== year:
                        return income['income']
            return f"not found"
    def savings(self, username=None, month=None, year=None):
        user = users_collection.find_one({"username": username})
        now = datetime.now()
        month = month or now.strftime("%B")
        year = year or now.year
        income_data = user.get('incomefield', [])
        income_sandy=0
        if income_data:
            for income in income_data:
                if income['month'] == month and income['year']== year:
                    income_sandy=income['income']
            if income_sandy==0:
                return f"No data found"
        total_expenses = 0
        if "transactions" in user and isinstance(user["transactions"], list):
            for trans in user["transactions"]:
                if trans["month"] == month and trans["year"] == year:
                    total_expenses += trans["amount"]
        return income_sandy-total_expenses
    

if __name__ == '__main__':
    fire.Fire(FinanceManager)
