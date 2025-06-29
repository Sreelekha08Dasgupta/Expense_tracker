# Expense Tracker Application
# This Python program allows users to add, edit, delete, view, and visualize personal expenses.
# Data is saved in a JSON file, and matplotlib is used to display graphical summaries.
from datetime import datetime
from collections import defaultdict
import json
import matplotlib.pyplot as plt

class Expense:
    """Represents a single expense entry with amount, category, and date."""
    def __init__(self, amount, category, date):
        self.amount = amount
        self.category = category
        self.date = date

    def __str__(self):
        return f"Category: {self.category}, Amount: ₹{self.amount}, Date: {self.date}"

    def to_dict(self):
        return {
            'amount': self.amount,
            'category': self.category,
            'date': self.date
        }

    @staticmethod
    def from_dict(data):
        return Expense(data['amount'], data['category'], data['date'])

class ExpenseTracker:
    """Handles all operations related to managing and analyzing expenses."""
    def __init__(self):
        self.expenses = []

    def validate_date(self, date_str):# Convert the entered amount to float and validate input
        """Validates whether the given string is in YYYY-MM-DD date format."""
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def add_expenses(self):
        """Prompts the user to input a new expense and saves it to the file."""
        try:
            # Convert the entered amount to float and validate input
            amount = float(input("Enter the amount of the expense: ").strip())
            category = input("Enter the category of the expense: ").strip()
            date = input("Enter the date (YYYY-MM-DD) or press Enter for today's date: ").strip()
            # Use today's date if the user doesn't provide one
            if not date:
                date = datetime.now().strftime("%Y-%m-%d")
            if not self.validate_date(date):
                print("Error: Invalid date format. Please use YYYY-MM-DD.")
                return
            # Create and add expense object to the list
            expense = Expense(amount, category, date)
            self.expenses.append(expense)
            print(f"Success: ₹{amount} added to category '{category}' on {date}.")
            self.save_to_file()
        except ValueError:
            print("Error: Invalid input. Please enter a numeric amount.")

    def view_summary(self):
        """Displays a summary of expenses based on user-selected criteria."""
        if not self.expenses:
            print("No expenses recorded yet.")
            return
        try:
            choice = int(input(
                "\nSelect an option:\n"
                "1. Total spending for a specific category\n"
                "2. Total overall spending\n"
                "3. Spending over time\n"
                "Your choice: ").strip())
        except ValueError:
            print("Error: Invalid input. Please enter a number.")
            return

        if choice == 1:
            category = input("Enter the category name: ").strip()
            total = sum(exp.amount for exp in self.expenses if exp.category.lower() == category.lower())
            print(f"Total spending in category '{category}': ₹{total:.2f}")
        elif choice == 2:
            # Total spending overall
            total = sum(exp.amount for exp in self.expenses)
            print(f"Total overall spending: ₹{total:.2f}")
        elif choice == 3:
            try:
                time_choice = int(input(
                    "Choose time period:\n"
                    "1. Daily Summary\n"
                    "2. Monthly Summary\n"
                    "3. Weekly Summary\n"
                    "Your choice: ").strip())
            except ValueError:
                print("Error: Invalid input. Please enter a number.")
                return

            summary = defaultdict(float)
            for expense in self.expenses:
                if not self.validate_date(expense.date):
                    print(f"Warning: Skipping invalid date format '{expense.date}'.")
                    continue
                date_obj = datetime.strptime(expense.date, "%Y-%m-%d")
                if time_choice == 1:
                    key = expense.date
                elif time_choice == 2:
                    key = date_obj.strftime("%Y-%m")
                elif time_choice == 3:
                    year = date_obj.year
                    week = date_obj.isocalendar()[1]
                    key = f"{year}-W{week}"
                else:
                    print("Error: Invalid choice.")
                    return
                summary[key] += expense.amount

            print("\nSpending summary over selected time period:")
            for period, amount in sorted(summary.items()):
                print(f"{period}: ₹{amount:.2f}")
        else:
            print("Error: Please choose a valid option (1, 2, or 3).")

    def save_to_file(self, filename="expenses.json"):
        """Saves all expenses to a JSON file."""
        with open(filename, 'w') as file:
            json.dump([exp.to_dict() for exp in self.expenses], file, indent=4)
        print(f"Data saved successfully to '{filename}'.")

    def load_from_file(self, filename="expenses.json"):
        """Loads expenses from a JSON file into the application."""
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                self.expenses = [Expense.from_dict(item) for item in data]
            print(f"Successfully loaded {len(self.expenses)} expense(s) from '{filename}'.")
        except FileNotFoundError:
            print("No existing data found. Starting a new record.")
        except json.JSONDecodeError:
            print("Error: Data file is corrupted. Starting with an empty list.")

    def delete_expense(self):
        """Allows the user to delete a specific expense by selecting it from the list."""
        if not self.expenses:
            print("No expenses available to delete.")
            return
        # Show expenses with index numbers
        for idx, exp in enumerate(self.expenses):
            print(f"{idx + 1}. {exp}")
        try:
            choice = int(input("Enter the number of the expense to delete: ").strip())
            if 1 <= choice <= len(self.expenses):
                removed = self.expenses.pop(choice - 1)
                print(f"Deleted: {removed}")
                self.save_to_file()
            else:
                print("Error: Invalid selection.")
        except ValueError:
            print("Error: Invalid input. Please enter a number.")

    def edit_expense(self):
        """Allows the user to edit a selected expense's details."""
        if not self.expenses:
            print("No expenses available to edit.")
            return
        for idx, exp in enumerate(self.expenses):
            print(f"{idx + 1}. {exp}")
        try:
            choice = int(input("Enter the number of the expense to edit: ").strip())
            if 1 <= choice <= len(self.expenses):
                expense = self.expenses[choice - 1]
                print(f"Editing expense: {expense}")
                new_amount = input("Enter new amount (or press Enter to keep current): ").strip()
                new_category = input("Enter new category (or press Enter to keep current): ").strip()
                new_date = input("Enter new date (YYYY-MM-DD) (or press Enter to keep current): ").strip()
                # Update fields if provided
                if new_amount:
                    try:
                        expense.amount = float(new_amount)
                    except ValueError:
                        print("Invalid amount entered. Keeping existing value.")
                if new_category:
                    expense.category = new_category
                if new_date:
                    if self.validate_date(new_date):
                        expense.date = new_date
                    else:
                        print("Invalid date format. Keeping existing date.")
                self.save_to_file()
                print("Expense updated successfully.")
            else:
                print("Error: Invalid selection.")
        except ValueError:
            print("Error: Invalid input. Please enter a number.")

    def graphical_summary(self):
        """Displays a bar chart of expenses grouped by category using matplotlib."""
        if not self.expenses:
            print("No data available for graphical summary.")
            return
        category_totals = defaultdict(float)
        for exp in self.expenses:
            category_totals[exp.category] += exp.amount
        # Prepare data for plotting
        categories = list(category_totals.keys())
        amounts = [category_totals[cat] for cat in categories]
        # Plot the bar chart
        plt.figure(figsize=(10, 6))
        plt.bar(categories, amounts, color='skyblue')
        plt.xlabel("Category")
        plt.ylabel("Total Expenses (₹)")
        plt.title("Expense Distribution by Category")
        plt.xticks(rotation=45)
        plt.grid(axis='y')
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":  
    tracker = ExpenseTracker()
    tracker.load_from_file()
    while True:
        print("\n================ Expense Tracker Menu ================")
        print("1. Add Expense")
        print("2. View Summary")
        print("3. Edit Expense")
        print("4. Delete Expense")
        print("5. Graphical Summary")
        print("6. Exit")
        choice = input("Enter your choice (1-6): ").strip()
        if choice == '1':
            tracker.add_expenses()
        elif choice == '2':
            tracker.view_summary()
        elif choice == '3':
            tracker.edit_expense()
        elif choice == '4':
            tracker.delete_expense()
        elif choice == '5':
            tracker.graphical_summary()
        elif choice == '6':
            print("Thank you for using the Expense Tracker. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")
