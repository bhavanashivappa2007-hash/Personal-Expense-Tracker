
import json
from abc import ABC, abstractmethod


# Abstract class
class Budget(ABC):

    @abstractmethod
    def check_budget(self):
        pass


# Expense class
class Expense:

    def __init__(self, name, category, amount):
        self.name = name
        self.category = category
        self.amount = amount

    def display(self):
        print(
            f"{self.name} | {self.category} | "
            f"Rs. {self.amount:.2f}"
        )

    def to_dict(self):
        return {
            "name": self.name,
            "category": self.category,
            "amount": self.amount
        }


# Parent class
class ExpenseTracker:

    def __init__(self):
        self.expenses = []
        self.load_expenses()

    # Load expenses
    def load_expenses(self):
        try:
            with open("expenses.json", "r") as file:
                data = json.load(file)

                for item in data:
                    expense = Expense(
                        item["name"],
                        item["category"],
                        item["amount"]
                    )
                    self.expenses.append(expense)

        except FileNotFoundError:
            self.expenses = []

        except (json.JSONDecodeError, KeyError, TypeError):
            print("Unable to read expense file.")

    # Save expenses
    def save_expenses(self):
        data = []

        for expense in self.expenses:
            data.append(expense.to_dict())

        with open("expenses.json", "w") as file:
            json.dump(data, file, indent=4)

    # Add expense
    def add_expense(self):
        print("\n--- Add Expense ---")

        name = input("Enter expense name: ").strip()
        category = input("Enter category: ").strip()

        if not name or not category:
            print("Name and category cannot be empty!")
            return

        try:
            amount = float(input("Enter amount: "))

            if amount <= 0:
                print("Amount must be greater than zero!")
                return

            expense = Expense(name, category, amount)
            self.expenses.append(expense)

            self.save_expenses()
            print("Expense added successfully!")

        except ValueError:
            print("Please enter a valid amount!")

        except OSError:
            self.expenses.pop()
            print("Unable to save the expense file!")

    # View expenses
    def view_expenses(self):
        print("\n--- All Expenses ---")

        if not self.expenses:
            print("No expenses found.")
            return

        for index, expense in enumerate(self.expenses, start=1):
            print(f"{index}. ", end="")
            expense.display()

    # Calculate total
    def total_expenses(self):
        total = sum(expense.amount for expense in self.expenses)
        print(f"\nTotal Expenses: Rs. {total:.2f}")

    # Delete expense
    def delete_expense(self):
        self.view_expenses()

        if not self.expenses:
            return

        try:
            number = int(input("Enter expense number to delete: "))

            if 1 <= number <= len(self.expenses):
                removed = self.expenses.pop(number - 1)

                try:
                    self.save_expenses()
                    print(f"{removed.name} deleted successfully!")

                except OSError:
                    self.expenses.insert(number - 1, removed)
                    print("Unable to save changes!")

            else:
                print("Invalid expense number!")

        except ValueError:
            print("Please enter a valid number!")

    # Parent method
    def check_budget(self):
        print("Budget feature is not available.")

    # Main menu
    def run(self):
        while True:
            print("\n===== PERSONAL EXPENSE TRACKER =====")
            print("1. Add Expense")
            print("2. View Expenses")
            print("3. Total Expenses")
            print("4. Delete Expense")
            print("5. Check Budget")
            print("6. Exit")

            choice = input("Enter your choice: ")

            if choice == "1":
                self.add_expense()

            elif choice == "2":
                self.view_expenses()

            elif choice == "3":
                self.total_expenses()

            elif choice == "4":
                self.delete_expense()

            elif choice == "5":
                self.check_budget()

            elif choice == "6":
                print("Thank you for using Personal Expense Tracker!")
                break

            else:
                print("Invalid choice! Please select 1 to 6.")


# Child class: Inheritance and Polymorphism
class BudgetTracker(ExpenseTracker, Budget):

    def __init__(self, budget):
        super().__init__()
        self.__budget = budget

    # Encapsulation
    def get_budget(self):
        return self.__budget

    # Polymorphism and Abstraction
    def check_budget(self):
        total = sum(expense.amount for expense in self.expenses)

        print(f"\nYour Budget: Rs. {self.__budget:.2f}")
        print(f"Total Expenses: Rs. {total:.2f}")

        if total > self.__budget:
            print("Warning! You have exceeded your budget.")

        else:
            print("You are within your budget!")


# Main program
if __name__ == "__main__":
    tracker = BudgetTracker(5000)
    tracker.run()
