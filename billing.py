import tkinter as tk
from tkinter import messagebox, simpledialog
import mysql.connector

# ------------------ Database Connection ------------------
class DBConnection:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='billing'
        )
        self.cursor = self.conn.cursor()

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()


# ------------------ OOP Design ------------------
class Person:
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone


class Customer(Person):
    def __init__(self, name, phone):
        super().__init__(name, phone)
        self.__balance = 0.0
        self.items = []

    def add_item(self, name, qty, price):
        self.items.append((name, qty, price))
        self.__balance += qty * price

    def get_balance(self):
        return self.__balance


# ------------------ Application Logic ------------------
class BillingApp:
    def __init__(self, root):
        self.root = root
        self.db = DBConnection()
        self.root.title("Billing Application")
        self.root.geometry("500x500")

        self.customer = None

        self.build_gui()

    def build_gui(self):
        tk.Label(self.root, text="Customer Name").pack()
        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack()

        tk.Label(self.root, text="Phone Number").pack()
        self.phone_entry = tk.Entry(self.root)
        self.phone_entry.pack()

        tk.Label(self.root, text="Item Name").pack()
        self.item_entry = tk.Entry(self.root)
        self.item_entry.pack()

        tk.Label(self.root, text="Quantity").pack()
        self.qty_entry = tk.Entry(self.root)
        self.qty_entry.pack()

        tk.Label(self.root, text="Price").pack()
        self.price_entry = tk.Entry(self.root)
        self.price_entry.pack()

        tk.Button(self.root, text="Add Item", command=self.add_item).pack(pady=5)
        tk.Button(self.root, text="Generate Bill", command=self.generate_bill).pack(pady=5)
        tk.Button(self.root, text="Delete Customer", command=self.delete_customer).pack(pady=5)
        tk.Button(self.root, text="Exit", command=self.root.quit).pack(pady=5)

    def add_item(self):
        try:
            name = self.name_entry.get()
            phone = self.phone_entry.get()

            if not name.isalpha():
                raise ValueError("Name must be alphabetic")
            if not phone.isdigit():
                raise ValueError("Phone must be numeric")

            if self.customer is None:
                self.customer = Customer(name, phone)

            item = self.item_entry.get()
            qty = int(self.qty_entry.get())
            price = float(self.price_entry.get())

            self.customer.add_item(item, qty, price)
            messagebox.showinfo("Success", "Item added!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def generate_bill(self):
        try:
            # Insert customer
            self.db.cursor.execute(
                "INSERT INTO customers (name, phone, balance) VALUES (%s, %s, %s)",
                (self.customer.name, self.customer.phone, self.customer.get_balance())
            )
            customer_id = self.db.cursor.lastrowid

            # Insert items
            for item in self.customer.items:
                self.db.cursor.execute(
                    "INSERT INTO items (customer_id, item_name, quantity, price) VALUES (%s, %s, %s, %s)",
                    (customer_id, item[0], item[1], item[2])
                )

            self.db.commit()

            # Generate bill file
            with open(f"{self.customer.name}_bill.txt", "w") as f:
                f.write(f"Customer: {self.customer.name}\nPhone: {self.customer.phone}\n")
                f.write("Items:\n")
                for item in self.customer.items:
                    f.write(f"{item[0]} - Qty: {item[1]} - Price: {item[2]}\n")
                f.write(f"\nTotal: ₹{self.customer.get_balance()}\n")

            messagebox.showinfo("Success", "Bill Generated and Saved!")
            self.customer = None  # reset for new customer
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_customer(self):
        try:
            cust_id = simpledialog.askinteger("Delete", "Enter Customer ID to delete:")
            if not cust_id:
                return

            confirm = messagebox.askyesno("Confirm", f"Are you sure to delete customer ID {cust_id}?")
            if confirm:
                self.db.cursor.execute("DELETE FROM items WHERE customer_id = %s", (cust_id,))
                self.db.cursor.execute("DELETE FROM customers WHERE id = %s", (cust_id,))
                self.db.commit()
                messagebox.showinfo("Deleted", f"Customer ID {cust_id} deleted.")
        except Exception as e:
            messagebox.showerror("Error", str(e))


# ------------------ Run Application ------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = BillingApp(root)
    root.mainloop()
