import mysql.connector as my

# Step 1: Connect to the database
obj = my.connect(
    host="localhost",
    user="root",  
    password="1234",  
    database="project"  
)
cur = obj.cursor()

# Step 2: Function to list categories available
def category():
    print("************Categories available are: **************\n")
    
    query = "SELECT DISTINCT cat FROM main_table"
    cur.execute(query)
    fetch = cur.fetchall()
    
    # Display available categories
    for i in fetch:
        print(i[0])
    
    print("\n")
    inpCategory = input("Enter your category: ")
    print("\nWe have the following " + inpCategory + ":\n")
    
    # Query to get products based on category
    query = "SELECT prod_name, price FROM main_table WHERE cat = '{}'".format(inpCategory)
    cur.execute(query)
    fetch = cur.fetchall()

    # Display product names and prices
    for i in fetch:
        print(i[0] + " -------------- PRICE: " + str(i[1]))
    
    print("---------------X----------------------------")

# Step 3: Function to list all products
def product():
    query = "SELECT prod_name, price FROM main_table"
    cur.execute(query)
    fetch = cur.fetchall()

    # Display all products and their prices
    for i in fetch:
        print(i[0] + " -------------- PRICE: " + str(i[1]))

    print("---------------X----------------------------")

# Step 4: Function to list products from a specific brand
def brand():
    print("*************Brands available are: ***************\n")
    
    query = "SELECT DISTINCT brand FROM main_table"
    cur.execute(query)
    fetch = cur.fetchall()

    # Display available brands
    for i in fetch:
        print(i[0])

    print("\n")
    inpBrand = input("What brand are you looking for? ")
    print("\nWe have the following available products from " + inpBrand + ":\n")
    
    # Query to get products based on brand
    query = "SELECT prod_name, price FROM main_table WHERE brand = '{}'".format(inpBrand)
    cur.execute(query)
    fetch = cur.fetchall()

    # Display product names and prices
    for i in fetch:
        print(i[0] + " ----------- PRICE: " + str(i[1]))

    print("---------------------------------------------------")

# Step 5: Function to place an order
def order():
    inpContact = input("Enter your 10-digit phone number: ")
    inpOrder = input("What do you want to order? ")
    
    # Query to get the quantity of the product
    query = "SELECT qty FROM main_table WHERE prod_name = '{}'".format(inpOrder)
    cur.execute(query)
    fetch = cur.fetchone()  # Fetch the quantity for the product

   
    if fetch[0] == 0:  # Check if the quantity is 0 (out of stock)
        print("OUT OF STOCK!!!!!!")
    else:
        # Query to get the product ID
        query = "SELECT prod_id FROM main_table WHERE prod_name = '{}'".format(inpOrder)
        cur.execute(query)
        fetch_id = cur.fetchone()  # Fetch the product ID

        # For subtracting from main_table only if quantity > 0
        query = "UPDATE main_table SET qty = qty - 1 WHERE prod_name = '{}'".format(inpOrder)
        cur.execute(query)
        obj.commit()

        # Get the maximum tid (transaction ID) from the order_table and increment it by 1
        query = "SELECT MAX(tid) FROM order_table"
        cur.execute(query)
        max_tid = cur.fetchone()[0] + 1  # Increment the tid by 1

        # Insert order into order_table with the new tid
        query = (
            "INSERT INTO order_table (tid, pid, pname,dispatch_date, customer_contact) VALUES\
                  ({}, {}, '{}',curdate(),'{}')".format(max_tid, fetch_id[0], inpOrder, inpContact)
        )
        cur.execute(query)
        obj.commit()

        print("Your order has been placed with transaction ID: " + str(max_tid))

# Step 6: Main program loop to interact with the user, with exit option
while True:
    print("WELCOME TO E-SHOP :) \n")
    print("Press 1 if you are looking for a category.")
    print("Press 2 if you are looking for a product.")
    print("Press 3 if you are looking for a brand.")
    print("Press 4 if you want to place an order.")
    print("Press 5 to exit.\n")

    try:
        inpInt = int(input("Enter your number: "))
        print("\n")
        if inpInt == 1:
            category()
        elif inpInt == 2:
            product()
        elif inpInt == 3:
            brand()
        elif inpInt == 4:
            order()
        elif inpInt == 5:
            print("Exiting the program. Goodbye!")
            break
        else:
            print("ERROR!!! Check your number.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")

