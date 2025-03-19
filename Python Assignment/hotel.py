"""
Restaurant Management System
CT108-3-1 Group Assignment
APU, 2024
"""

import os
from datetime import datetime

# ========== CONSTANTS ==========
USER_FILE = "users.txt"
MENU_FILE = "menu.txt"
ORDERS_FILE = "orders.txt"
FEEDBACK_FILE = "feedback.txt"
INGREDIENTS_FILE = "ingredients.txt"
MAX_LOGIN_ATTEMPTS = 3
ROLES = ["Admin", "Manager", "Chef", "Customer"]

# ========== FILE HANDLING ==========
def read_data(filename):
    """Generic function to read data from files"""
    data = []
    try:
        with open(filename, "r") as f:
            for line in f:
                if line.strip():
                    data.append(line.strip().split(','))
    except FileNotFoundError:
        pass
    return data

def write_data(filename, data):
    """Generic function to write data to files"""
    with open(filename, "w") as f:
        for item in data:
            f.write(','.join(item) + '\n')

#======Registeration======
def register_customer():
    """Allow a customer to register an account"""
    users = read_data(USER_FILE)  # Read existing users from file
    
    print("\nCustomer Registration")
    
    # Get new customer details
    username = input("Enter username: ").strip().lower()  # Normalize to lowercase
    if any(user[0].strip().lower() == username for user in users):
        print("Username already exists! Please choose another.")
        return
    
    password = input("Enter password: ").strip()
    confirm_password = input("Confirm password: ").strip()
    
    # Password confirmation
    if password != confirm_password:
        print("Passwords do not match!")
        return

    # Add the new customer to the user list
    users.append([username, password, "Customer"])
    
    # Write updated user data to file
    write_data(USER_FILE, users)
    
    print("Registration successful! You can now log in as a Customer.")

#========feedback==============
def submit_feedback(username):
    """Allow customer to give feedback with or without an order ID"""
    print("\n📝 Feedback Form")

    # Ask if they want to provide an Order ID (optional)
    order_id = input("Enter Order ID (or press Enter to skip): ").strip()
    
    # Ensure the order ID exists if provided
    orders = read_data(ORDERS_FILE)
    if order_id and not any(order[0] == order_id for order in orders):
        print("⚠️ Order ID not found! Proceeding without an Order ID.")

    # Ask for rating
    while True:
        rating = input("Rate us (1-5 stars): ").strip()
        if rating in ['1', '2', '3', '4', '5']:
            break
        print("⚠️ Invalid input! Please enter a number between 1 and 5.")

    # Ask for feedback comments
    comments = input("Write your feedback: ").strip()
    
    if not comments:
        print("⚠️ Feedback cannot be empty!")
        return

    # Save feedback
    feedback_data = read_data(FEEDBACK_FILE)
    feedback_id = str(len(feedback_data) + 1)
    feedback_entry = [feedback_id, username, order_id if order_id else "N/A", rating, comments, datetime.now().strftime("%Y-%m-%d")]

    write_data(FEEDBACK_FILE, feedback_data + [feedback_entry])

    print("\n✅ Thank you for your feedback!")

def view_feedback():
    """Admin/Manager: View all customer feedback"""
    feedbacks = read_data(FEEDBACK_FILE)
    
    if not feedbacks:
        print("No feedback available.")
        return
    
    print("\nCustomer Feedback:")
    for feedback in feedbacks:
        if len(feedback) != 5:  # Ensure correct structure
            print(f"⚠️ Skipping malformed feedback entry: {feedback}")
            continue  # Skip incorrect entries
        
        order_id, username, rating, comments, timestamp = feedback
        print(f"Order ID: {order_id}, Customer: {username}, Rating: {rating}, Date: {timestamp}")
        print(f"Comments: {comments if comments else 'No comments'}\n")

#=============== Profile Section ==============================
def update_profile(username):
    """Allow users to update their profile information"""
    users = read_data(USER_FILE)

    for user in users:
        if user[0] == username:
            print("\nUpdate Profile:")
            new_username = input(f"Enter new username (current: {username}): ").strip()
            
            # Ensure username is unique
            if new_username and any(u[0] == new_username for u in users):
                print("⚠️ Username already taken! Choose another.")
                return

            new_password = input("Enter new password (leave blank to keep current): ").strip()
            confirm_password = input("Confirm new password: ").strip()

            if new_password and new_password != confirm_password:
                print("⚠️ Passwords do not match!")
                return

            # Update the user details
            user[0] = new_username if new_username else user[0]
            user[1] = new_password if new_password else user[1]

            write_data(USER_FILE, users)
            print("✅ Profile updated successfully!")
            return

    print("⚠️ User not found!")

def update_customer_profile(username):
    """Allow customer to update their profile information (username and password only)"""
    users = read_data(USER_FILE)

    for user in users:
        if user[0] == username:
            print("\nUpdate Profile:")
            new_username = input(f"Enter new username (current: {username}): ").strip()
            
            # Ensure username is unique
            if new_username and any(u[0] == new_username for u in users):
                print("⚠️ Username already taken! Choose another.")
                return

            new_password = input("Enter new password (leave blank to keep current): ").strip()
            confirm_password = input("Confirm new password: ").strip()

            if new_password and new_password != confirm_password:
                print("⚠️ Passwords do not match!")
                return

            # Update the user details
            user[0] = new_username if new_username else user[0]
            user[1] = new_password if new_password else user[1]

            write_data(USER_FILE, users)
            print("✅ Profile updated successfully!")
            return

    print("⚠️ User not found!")

# ========== INGREDIENT MANAGEMENT ==========
def manage_ingredient_requests(username):
    """Chef: Add/Edit/Delete ingredient requests"""
    while True:
        print("\n🍽 Manage Ingredient Requests")
        print("1. Add New Request")
        print("2. Edit Existing Request")
        print("3. Delete Request")
        print("4. Return to Chef Menu")
        choice = input("Enter choice: ")

        if choice == '1':
            add_ingredient_request(username)
        elif choice == '2':
            edit_ingredient_request(username)
        elif choice == '3':
            delete_ingredient_request(username)
        elif choice == '4':
            break
        else:
            print("Invalid choice!")

def add_ingredient_request(username):
    """Chef: Add new ingredient request"""
    ingredients = read_data(INGREDIENTS_FILE)
    ingredient_id = str(len(ingredients) + 1)
    
    name = input("Enter ingredient name: ").strip()
    quantity = input("Enter quantity needed: ").strip()
    
    if not quantity.isdigit():
        print("⚠️ Invalid quantity! Must be a whole number.")
        return

    new_request = [
        ingredient_id,
        name,
        quantity,
        "Requested",  # Default status
        username,
        datetime.now().strftime("%Y-%m-%d")
    ]
    
    write_data(INGREDIENTS_FILE, ingredients + [new_request])
    print(f"✅ Successfully requested {quantity} units of {name}")

def edit_ingredient_request(username):
    """Chef: Edit existing ingredient request"""
    ingredients = read_data(INGREDIENTS_FILE)
    chef_requests = [req for req in ingredients if req[4] == username and req[3] == "Requested"]
    
    if not chef_requests:
        print("No editable requests found (only 'Requested' status can be edited).")
        return
    
    print("\nYour Active Requests:")
    for req in chef_requests:
        print(f"ID: {req[0]} | {req[1]} - {req[2]} units | Requested on {req[5]}")

    req_id = input("Enter request ID to edit: ").strip()
    request = next((req for req in chef_requests if req[0] == req_id), None)
    
    if not request:
        print("⚠️ Invalid ID or request not editable")
        return

    new_name = input(f"Enter new name ({request[1]}): ").strip() or request[1]
    new_qty = input(f"Enter new quantity ({request[2]}): ").strip() or request[2]
    
    if not new_qty.isdigit():
        print("⚠️ Quantity must be a number!")
        return

    # Update in full ingredients list
    for i in range(len(ingredients)):
        if ingredients[i][0] == req_id:
            ingredients[i][1] = new_name
            ingredients[i][2] = new_qty
            break
    
    write_data(INGREDIENTS_FILE, ingredients)
    print("✅ Request updated successfully")

def delete_ingredient_request(username):
    """Chef: Delete ingredient request"""
    ingredients = read_data(INGREDIENTS_FILE)
    chef_requests = [req for req in ingredients if req[4] == username]
    
    if not chef_requests:
        print("You have no active requests")
        return
    
    print("\nYour Requests:")
    for req in chef_requests:
        print(f"ID: {req[0]} | {req[1]} - {req[2]} units | Status: {req[3]}")
    
    req_id = input("Enter request ID to delete: ").strip()
    
    # Check ownership before deletion
    updated_requests = [req for req in ingredients if not (req[0] == req_id and req[4] == username)]
    
    if len(updated_requests) == len(ingredients):
        print("⚠️ Request not found or not authorized")
        return
    
    write_data(INGREDIENTS_FILE, updated_requests)
    print("✅ Request deleted successfully")

def view_ingredient_requests():
    """Manager: View all ingredient requests"""
    ingredients = read_data(INGREDIENTS_FILE)
    
    if not ingredients:
        print("No ingredient requests found")
        return
    
    print("\n📋 All Ingredient Requests:")
    for req in ingredients:
        status_color = "🟢" if req[3] == "Approved" else "🟡" if req[3] == "Requested" else "🔴"
        print(f"{status_color} ID: {req[0]}")
        print(f"   Ingredient: {req[1]}")
        print(f"   Quantity: {req[2]}")
        print(f"   Requested by: {req[4]} on {req[5]}")
        print(f"   Status: {req[3]}")
        print("-" * 40)

#======== Order =============
def place_order(username):
    """Customer: Place a new order"""
    menu = read_data(MENU_FILE)
    
    if not menu:
        print("The menu is currently empty. Please try again later.")
        return

    print("\n📋 Menu:")
    for item in menu:
        print(f"{item[0]}. {item[1]} - RS{item[2]}")

    order_items = []
    
    while True:
        item_id = input("\nEnter item ID to order (or type 'done' to finish): ").strip()
        if item_id.lower() == 'done':
            break

        # Find item by ID
        item = next((m for m in menu if m[0] == item_id), None)
        if not item:
            print("⚠️ Invalid item ID! Please try again.")
            continue

        quantity = input(f"Enter quantity for {item[1]}: ").strip()
        if not quantity.isdigit() or int(quantity) <= 0:
            print("⚠️ Invalid quantity! Please enter a valid number.")
            continue

        quantity = int(quantity)
        order_items.append((item_id, quantity, float(item[2])))

    if not order_items:
        print("⚠️ No items selected! Order not placed.")
        return

    # Calculate total price
    total = sum(price * quantity for _, quantity, price in order_items)

    # Generate Order ID
    orders = read_data(ORDERS_FILE)
    order_id = str(len(orders) + 1)

    # Format order details
    order_details = ';'.join([f"{item_id}:{quantity}" for item_id, quantity, _ in order_items])
    
    # Save order
    new_order = [
        order_id,    # Order ID
        username,    # Customer Name
        order_details,  # Ordered Items
        f"{total:.2f}",  # Total Price
        "Pending",  # Order Status
        datetime.now().strftime("%Y-%m-%d"),  # Date
        ""  # Additional Notes
    ]

    write_data(ORDERS_FILE, orders + [new_order])
    
    print(f"\n✅ Order placed successfully! Order ID: {order_id}")
    print(f"💰 Total Price: RS{total:.2f}")
    print("📌 Status: Pending")
#========View Order  ========
def view_order_status(username):
    """Customer: View the status of their orders"""
    orders = read_data(ORDERS_FILE)
    
    user_orders = [order for order in orders if order[1] == username]  # Filter by username

    if not user_orders:
        print("\nYou have no orders yet.")
        return

    print("\n📦 Your Orders:")
    for order in user_orders:
        order_id, _, items, total, status, date, notes = order
        print(f"🆔 Order ID: {order_id} | 🗓 Date: {date} | 💰 Total: RS{total} | 📌 Status: {status}")
        print(f"🛒 Items: {items}")
        if notes:
            print(f"📝 Notes: {notes}")
        print("-" * 50)

#================= sales report ============
def view_sales_report():
    """Admin: View sales summary"""
    orders = read_data(ORDERS_FILE)
    
    if not orders:
        print("\nNo sales data available.")
        return

    total_sales = 0.0
    completed_orders = 0
    item_sales = {}

    print("\n📊 Sales Report")
    
    for order in orders:
        order_id, username, items, total, status, date, notes = order
        
        if status == "Completed":
            total_sales += float(total)
            completed_orders += 1
            
            # Count item sales
            for item in items.split(';'):
                item_id, quantity = item.split(':')
                quantity = int(quantity)
                if item_id in item_sales:
                    item_sales[item_id] += quantity
                else:
                    item_sales[item_id] = quantity

    print(f"\n✅ Total Completed Orders: {completed_orders}")
    print(f"💰 Total Sales Revenue: RS{total_sales:.2f}")
    
    # Show most popular items
    print("\n🍽️ Most Ordered Items:")
    menu = read_data(MENU_FILE)
    menu_dict = {item[0]: item[1] for item in menu}  # Map item_id to name
    
    for item_id, quantity in sorted(item_sales.items(), key=lambda x: x[1], reverse=True):
        item_name = menu_dict.get(item_id, "Unknown Item")
        print(f"📌 {item_name}: {quantity} orders")

    print("\n📅 Sales by Date:")
    unique_dates = sorted(set(order[5] for order in orders if order[4] == "Completed"))
    for date in unique_dates:
        date_sales = sum(float(order[3]) for order in orders if order[4] == "Completed" and order[5] == date)
        print(f"{date}: RS{date_sales:.2f}")


# ========== AUTHENTICATION ==========
def login():
    """Handle user login with attempt tracking"""
    attempts = 0
    while attempts < MAX_LOGIN_ATTEMPTS:
        print("\n1. Log in")
        print("2. Register as Customer")
        choice = input("Enter choice: ")

        if choice == "2":
            register_customer()
            continue  # After registration, allow the user to try logging in

        username = input("Username: ").strip().lower()  # Normalize input
        password = input("Password: ").strip()

        users = read_data(USER_FILE)
        for user in users:
            stored_username = user[0].strip().lower()  # Normalize stored data
            stored_password = user[1].strip()
            role = user[2].strip()

            if username == stored_username and password == stored_password:
                if role not in ROLES:  # Prevent invalid roles
                    print("Error: Invalid role detected in user file!")
                    return None, None
                
                print(f"Login successful! Role: {role}")
                return role, user[0]  # Return original (case-sensitive) username
        
        print(f"Invalid credentials. Attempts left: {MAX_LOGIN_ATTEMPTS - attempts - 1}")
        attempts += 1

    print("Too many failed attempts. Exiting.")
    return None, None


# ========== ADMIN FUNCTIONS ==========
def manage_staff():
    """Admin: Add/Edit/Delete staff accounts"""
    users = read_data(USER_FILE)
    
    print("\nStaff Management")
    print("1. Add Staff")
    print("2. Edit Staff")
    print("3. Delete Staff")
    choice = input("Enter choice: ")
    
    if choice == '1':
        # Add Staff
        add_staff(users)
        
    elif choice == '2':
        # Edit Staff
        edit_staff(users)
        
    elif choice == '3':
        # Delete Staff
        delete_staff(users)
        
    else:
        print("Invalid choice. Please try again.")

def add_staff(users):
    """Add a new staff member"""
    username = input("Enter new username: ")
    if any(user[0] == username for user in users):
        print("Username already exists!")
        return

    password = input("Enter password: ")
    role = input("Enter role (Manager/Chef): ")
    if role not in ["Manager", "Chef"]:
        print("Invalid role!")
        return

    users.append([username, password, role])
    write_data(USER_FILE, users)
    print("Staff added successfully!")

def edit_staff(users):
    """Edit an existing staff member's details"""
    username = input("Enter the username of the staff member to edit: ")
    
    # Find the staff member to edit
    for user in users:
        if user[0] == username:
            print(f"Editing {username}'s details...")
            new_username = input(f"Enter new username (current: {user[0]}): ").strip()
            new_password = input("Enter new password: ").strip()
            new_role = input(f"Enter new role (current: {user[2]}): ").strip()

            # Update only if a new value is provided
            if new_username:
                user[0] = new_username
            if new_password:
                user[1] = new_password
            if new_role:
                if new_role in ["Manager", "Chef"]:
                    user[2] = new_role
                else:
                    print("Invalid role!")
                    return
            
            write_data(USER_FILE, users)
            print(f"Staff details for {username} updated successfully!")
            return
    
    print("Staff member not found!")

def delete_staff(users):
    """Delete a staff member"""
    username = input("Enter the username of the staff member to delete: ")

    # Find and delete the staff member
    for user in users:
        if user[0] == username:
            users.remove(user)
            write_data(USER_FILE, users)
            print(f"Staff member {username} deleted successfully!")
            return
    
    print("Staff member not found!")

def read_data(filename):
    """Read data from file"""
    try:
        with open(filename, 'r') as file:
            return [line.strip().split(",") for line in file.readlines()]
    except FileNotFoundError:
        return []

def write_data(filename, data):
    """Write data to file"""
    with open(filename, 'w') as file:
        for line in data:
            file.write(",".join(line) + "\n")


# ========== MANAGER FUNCTIONS ==========
def manage_menu():
    """Manager: Add/Edit/Delete menu items"""
    menu = read_data(MENU_FILE)

    print("\nMenu Management")
    print("1. Add Item")
    print("2. Edit Item")
    print("3. Delete Item")
    choice = input("Enter choice: ")

    if choice == '1':  #  Add Menu Item
        item_id = input("Enter item ID: ")
        if any(item[0] == item_id for item in menu):
            print("Item ID already exists!")
            return

        name = input("Enter item name: ")
        price = input("Enter price: ")
        try:
            float(price)
        except ValueError:
            print("Invalid price!")
            return

        menu.append([item_id, name, price])
        write_data(MENU_FILE, menu)
        print("Menu item added successfully!")

    elif choice == '2':  # ✅ Edit Menu Item
        item_id = input("Enter item ID to edit: ")
        for item in menu:
            if item[0] == item_id:
                new_name = input(f"Enter new name (current: {item[1]}): ") or item[1]
                new_price = input(f"Enter new price (current: {item[2]}): ")
                
                try:
                    new_price = float(new_price) if new_price else item[2]
                except ValueError:
                    print("Invalid price!")
                    return

                item[1], item[2] = new_name, str(new_price)
                write_data(MENU_FILE, menu)
                print("Menu item updated successfully!")
                return

        print("Item ID not found!")

    elif choice == '3':  # ✅ Delete Menu Item
        item_id = input("Enter item ID to delete: ")
        new_menu = [item for item in menu if item[0] != item_id]

        if len(new_menu) == len(menu):
            print("Item ID not found!")
            return

        write_data(MENU_FILE, new_menu)
        print("Menu item deleted successfully!")

# ========== CHEF FUNCTIONS ==========
def view_orders():
    """Chef: View all active orders"""
    orders = read_data(ORDERS_FILE)
    print("\nActive Orders:")
    for order in orders:
        if order[4] in ["Pending", "In Progress"]:
            print(f"Order {order[0]} - Status: {order[4]} - Items: {order[2]}")

def update_order_status():
    # Read orders from the file
    orders = read_data(ORDERS_FILE)
    print("\nActive Orders:")
    for order in orders:
        # Display orders with status "Pending" or "In Progress"
        if order[4] in ["Pending", "In Progress"]:
            print(f"Order ID: {order[0]} - Status: {order[4]} - Items: {order[2]}")
    
    # Prompt for an Order ID to update
    order_id = input("Enter Order ID to update status: ")
    # Prompt for the new status
    new_status = input("Enter new status (Pending, In Progress, Completed): ")

    # Validate the new status
    if new_status not in ["Pending", "In Progress", "Completed"]:
        print("Invalid status!")
        return

    # Update the status of the selected order
    order_found = False
    for order in orders:
        if order[0] == order_id:
            order[4] = new_status  # Update the status field
            order_found = True
            break

    if order_found:
        # Write the updated order list back to the file
        write_data(ORDERS_FILE, orders)
        print(f"Order {order_id} status updated to {new_status}!")
    else:
        print("Order ID not found!")
   

# ========== CUSTOMER FUNCTIONS ==========
def place_order(username):
    """Customer: Place new order"""
    menu = read_data(MENU_FILE)
    print("\nMenu:")
    for item in menu:
        print(f"{item[0]}. {item[1]} - RS{item[2]}")

    order_items = []
    while True:
        item_id = input("Enter item ID (or 'done' to finish): ")
        if item_id.lower() == 'done':
            break

        # Find item by ID instead of using index
        item = next((m for m in menu if m[0] == item_id), None)
        if not item:
            print("Invalid item ID!")
            continue

        quantity = input("Enter quantity: ")
        if not quantity.isdigit():
            print("Invalid quantity!")
            continue

        order_items.append((item_id, int(quantity), float(item[2])))

    if not order_items:
        print("No items selected!")
        return

    # Corrected total price calculation
    total = sum(price * quantity for _, quantity, price in order_items)

    orders = read_data(ORDERS_FILE)
    order_id = str(len(orders) + 1)
    new_order = [
        order_id,
        username,
        ';'.join([f"{item_id}:{quantity}" for item_id, quantity, _ in order_items]),
        f"{total:.2f}",
        "Pending",
        datetime.now().strftime("%Y-%m-%d"),
        ""
    ]

    write_data(ORDERS_FILE, orders + [new_order])
    print(f"Order placed successfully! Total: RS{total:.2f}")


# ========== MENUS ==========
def admin_menu(username):
    while True:
        print(f"\nAdmin Menu ({username})")
        print("1. Manage Staff")
        print("2. View Sales Report")
        print("3. View Feedback")
        print("4. Update Profile")  # ✅ Added
        print("5. Logout")
        
        choice = input("Enter choice: ")
        if choice == '1':
            manage_staff()
        elif choice == '2':
            view_sales_report()
        elif choice == '3':
            view_feedback()
        elif choice == '4':  # ✅ Added
            update_profile(username)
        elif choice == '5':
            break


def manager_menu(username):
    while True:
        print(f"\nManager Menu ({username})")
        print("1. Manage Menu")
        print("2. View Orders")
        print("3. View Feedback")
        print("4. View Ingredient Requests")  # New option
        print("5. Update Profile")
        print("6. Logout")
        
        choice = input("Enter choice: ")
        if choice == '1':
            manage_menu()
        elif choice == '2':
            view_orders()
        elif choice == '3':
            view_feedback()
        elif choice == '4':
            view_ingredient_requests()  # New feature
        elif choice == '5':
            update_profile(username)
        elif choice == '6':
            break

def chef_menu(username):
    while True:
        print(f"\nChef Menu ({username})")
        print("1. View Orders")
        print("2. Update Order Status")
        print("3. Manage Ingredient Requests")  # New option
        print("4. Update Profile")
        print("5. Logout")
        
        choice = input("Enter choice: ")
        if choice == '1':
            view_orders()
        elif choice == '2':
            update_order_status()
        elif choice == '3':
            manage_ingredient_requests(username)  # New feature
        elif choice == '4':
            update_profile(username)
        elif choice == '5':
            break

def customer_menu(username):
    while True:
        print(f"\nCustomer Menu ({username})")
        print("1. Place Order")
        print("2. View Order Status")
        print("3. Submit Feedback")  # Added feedback option
        print("4. Update Profile")
        print("5. Logout")
        
        choice = input("Enter choice: ")
        if choice == '1':
            place_order(username)
        elif choice == '2':
            view_order_status(username)
        elif choice == '3':  # Feedback option
            submit_feedback(username)
        elif choice == '4':
            update_customer_profile(username)
        elif choice == '5':
            break

# ========== MAIN PROGRAM ==========
def main():
    print("=== Restaurant Management System ===")
    
    while True:
        role, username = login()
        if not role:
            continue
        if role == "Admin":
            admin_menu(username)
        elif role == "Manager":
            manager_menu(username)
        elif role == "Chef":
            chef_menu(username)
        elif role == "Customer":
            customer_menu(username)
        else:
            print("Invalid user role!")

if __name__ == "__main__":
    # Initialize all required files
    for file in [USER_FILE, MENU_FILE, ORDERS_FILE, FEEDBACK_FILE, INGREDIENTS_FILE]:
        if not os.path.exists(file):
            open(file, 'w').close()
    
    # Create default admin if none exists
    if not read_data(USER_FILE):
        write_data(USER_FILE, [["admin", "admin123", "Admin"]])

    # Initialize feedback file if it doesn't exist
    if not os.path.exists(FEEDBACK_FILE):
        open(FEEDBACK_FILE, 'w').close()

    
    main()