"""
Program: Module 08 Final Project Submission
Creator: Alicia Davis
Last time updated: 12/14/2024
Purpose: A pizza restaurant management system
"""

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Variables for order details
order_details = {
    "size": "",
    "toppings": [],
    "quantity": 0,
    "total_price": 0.0
}

# Pricing constants
SIZE_PRICES = {"Small": 8.99, "Medium": 12.99, "Large": 16.99}
TOPPING_PRICE = 1.50
TAX_RATE = 0.07

# Functions for application
def calculate_total():
    # Calculate the total cost based on the size, toppings, quantity, and tax
    size_price = SIZE_PRICES.get(order_details["size"], 0)
    toppings_price = len(order_details["toppings"]) * TOPPING_PRICE
    subtotal = (size_price + toppings_price) * order_details["quantity"]
    total = subtotal + (subtotal * TAX_RATE)
    return round(total, 2)

def add_to_cart(size, toppings, quantity):
    # Add selected pizza details to the cart
    if not size or quantity <= 0:
        messagebox.showerror("Input Error", "Please select a size and enter a valid quantity.")
        return

    order_details["size"] = size
    order_details["toppings"] = toppings
    order_details["quantity"] = quantity
    order_details["total_price"] = calculate_total()

    messagebox.showinfo("Success", "Pizza added to cart!")

def show_summary(window):
    # Transition to the order summary window
    window.destroy()
    summary_window()

def reset_order():
    # Reset the order details to start fresh
    global order_details
    order_details = {"size": "", "toppings": [], "quantity": 0, "total_price": 0.0}

def exit_app():
    # Confirm, exit and close the app
    if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
        app.quit()

# GUI Windows
def main_menu():
    def navigate_to_order():
        # Go to the order window
        main_window.destroy()
        order_window()

    main_window = tk.Tk()
    main_window.title("QuickPizza Main Menu")
    main_window.geometry("400x300")

    tk.Label(main_window, text="Welcome to QuickPizza!", font=("Helvetica", 16)).pack(pady=20)
    tk.Button(main_window, text="Order Pizza", command=navigate_to_order, width=20, height=2).pack(pady=10)
    tk.Button(main_window, text="Exit", command=exit_app, width=20, height=2).pack(pady=10)

    main_window.mainloop()

def order_window():
    def add_to_order():
        # Retrieve the selected size
        size = size_var.get() #This gets the value from the Radiobutton (Small, Medium, Large)

        # Make sure quantity is entered correctly, and handles errors
        try:
            quantity = int(quantity_entry.get())
            if quantity <= 0:
                raise ValueError("Quantity must be a positive number.")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid quantity.")
            return

        if not size or quantity <= 0: # Make sure size has been selected
            messagebox.showerror("Input Error", "Please select a size and enter a valid quantity.")
            return
        
        # Collect selected toppings
        selected_toppings = [t for t, v in toppings_vars.items() if v.get() == 1]

        # Add to cart
        add_to_cart(size, selected_toppings, quantity)

    def go_to_summary():
        # Navigate to the summary window
        show_summary(order_window)

    order_window = tk.Tk()
    order_window.title("Order Your Pizza")
    order_window.geometry("400x500")

    # Label and radiobuttons for size
    tk.Label(order_window, text="Select Pizza Size:", font=("Helvetica", 12)).pack(pady=10)

    size_var = tk.StringVar(value="Small") 

    for size in SIZE_PRICES.keys():
        tk.Radiobutton(order_window, text=f"{size} (${SIZE_PRICES[size]})", variable=size_var, value=size).pack(anchor="w", padx=20)

    # Labe; amd checkbuttons for toppings
    tk.Label(order_window, text="Select Toppings ($1.50 each):", font=("Helvetica", 12)).pack(pady=10)

    toppings_vars = {}    # Creating the dictionary to hold toppings' variables
    for topping in ["Pepperoni", "Mushrooms", "Onions", "Sausage", "Bacon"]:
        toppings_vars[topping] = tk.IntVar()   # Establish IntVar for each topping
        tk.Checkbutton(order_window, text=topping, variable=toppings_vars[topping]).pack(anchor="w", padx=20)

    # Entry for quantity
    tk.Label(order_window, text="Enter Quantity:", font=("Helvetica", 12)).pack(pady=10)
    quantity_entry = tk.Entry(order_window)
    quantity_entry.pack()

    # Add to cart button
    tk.Button(order_window, text="Add to Cart", command=add_to_order, width=20, height=2).pack(pady=10)
    tk.Button(order_window, text="View Order Summary", command=go_to_summary, width=20, height=2).pack(pady=10)
    tk.Button(order_window, text="Back to Main Menu", command=lambda: [order_window.destroy(), main_menu()], width=20, height=2).pack(pady=10)

    order_window.mainloop()

def summary_window():
    summary_window = tk.Tk()
    summary_window.title("Order Summary")
    summary_window.geometry("400x400")

    tk.Label(summary_window, text="Order Summary", font=("Helvetica", 16)).pack(pady=10)

    # Display the current order details
    tk.Label(summary_window, text=f"Size: {order_details['size']}").pack(anchor="w", padx=20)
    tk.Label(summary_window, text=f"Toppings: {', '.join(order_details['toppings'])}").pack(anchor="w", padx=20)
    tk.Label(summary_window, text=f"Quantity: {order_details['quantity']}").pack(anchor="w", padx=20)
    tk.Label(summary_window, text=f"Total Price: ${order_details['total_price']}").pack(anchor="w", padx=20)

    tk.Button(summary_window, text="Place Another Order", command=lambda: [summary_window.destroy(), reset_order(), main_menu()], width=20, height=2).pack(pady=10)
    tk.Button(summary_window, text="Exit", command=exit_app, width=20, height=2).pack(pady=10)

    summary_window.mainloop()

# Run the application
if __name__ == "__main__":
    app = tk.Tk()
    app.withdraw() # Hide the starting Tkinter window
    main_menu()
