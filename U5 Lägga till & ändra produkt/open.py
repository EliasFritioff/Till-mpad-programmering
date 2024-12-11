import csv
import os
import locale

def load_data(filename): 
    products = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            id = int(row['id'])
            name = row['name']
            desc = row['desc']
            price = float(row['price'])
            quantity = int(row['quantity'])
            
            products.append(
                {
                    "id": id,
                    "name": name,
                    "desc": desc,
                    "price": price,
                    "quantity": quantity
                }
            )
    return products

def save_data(filename, products):
    with open(filename, 'w', newline='') as file:
        fieldnames = ['id', 'name', 'desc', 'price', 'quantity']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        
        for product in products:
            writer.writerow(product)

def get_products(products): 
    product_list = []
    for index, product in enumerate(products):
        product_info = f"{index + 1}. Product: {product['name']} \t {product['desc']} \t {product['price']} kr \t Quantity: {product['quantity']}"
        product_list.append(product_info)
    
    return "\n".join(product_list)

def get_product_by_id(products, product_id): 
    for index, product in enumerate(products):
        if product['id'] == product_id:
           return f"Product {index + 1}: {product['name']} \t {product['desc']} \t {product['price']} kr \t Quantity: {product['quantity']}"
    return "Product not found."

def add_product(products, filename, name, desc, price, quantity):
    if products:
        new_id = max(product['id'] for product in products) + 1
    else:
        new_id = 1
    
    new_product = {
        "id": new_id,
        "name": name,
        "desc": desc,
        "price": price,
        "quantity": quantity
    }
    
    products.append(new_product)
    save_data(filename, products)
    
    print(f"Produkten '{name}' har lagts till.")

def remove_product(products, filename, product_id):
    for product in products:
        if product['id'] == product_id:
            products.remove(product)
            save_data(filename, products)
            print(f"Produkten med ID {product_id} har tagits bort.")
            return
    print(f"Produkten med ID {product_id} hittades inte.")

def edit_product(products, filename, product_id):
    for product in products:
        if product['id'] == product_id:
            print(f"Redigerar produkt med ID {product_id}:")
            new_name = input(f"Ange nytt namn för {product['name']} (tryck Enter för att behålla): ") or product['name']
            new_desc = input(f"Ange ny beskrivning för {product['desc']} (tryck Enter för att behålla): ") or product['desc']
            new_price = input(f"Ange nytt pris för {product['price']} (tryck Enter för att behålla): ")
            new_price = float(new_price) if new_price else product['price']
            new_quantity = input(f"Ange nytt antal för {product['quantity']} (tryck Enter för att behålla): ")
            new_quantity = int(new_quantity) if new_quantity else product['quantity']
            
            product['name'] = new_name
            product['desc'] = new_desc
            product['price'] = new_price
            product['quantity'] = new_quantity
            
            save_data(filename, products)
            print(f"Produkten med ID {product_id} har uppdaterats.")
            return
    print(f"Produkten med ID {product_id} hittades inte.")

def menu():
    print("\n--- MENY ---")
    print("1. Visa produkter")
    print("2. Lägg till produkt")
    print("3. Ta bort produkt")
    print("4. Ändra produkt")
    choice = input("Välj ett alternativ (1-4): ")
    return choice

def view_products(products):
    for product in products:
        print(f"ID: {product['id']} - {product['name']} \t {product['desc']} \t {product['price']} kr \t Quantity: {product['quantity']}","\n")

# Laddar produkter från CSV-fil.
products = load_data("db_products.csv")

# Produkter visas när programmet startar.
view_products(products)

while True:
    choice = menu()

    if choice == '1':
        os.system('cls')
        view_products(products)

    elif choice == '2':
        os.system('cls')
        view_products(products)
        new_product_name = input('Ange den nya produktens namn: ')
        new_product_desc = input(f"Ange en ny beskrivning för {new_product_name}: ")
        new_product_price = float(input(f"Ange ett pris för {new_product_name}: "))
        new_product_quantity = int(input(f"Ange hur många {new_product_name} som existerar: "))
        add_product(products, "db_products.csv", new_product_name, new_product_desc, new_product_price, new_product_quantity)
        
        # Visar den uppdaterade listan.
        view_products(products)

    elif choice == '3':
        os.system('cls')
        view_products(products)
        product_id = int(input("Ange ID för produkten som ska tas bort: "))
        remove_product(products, "db_products.csv", product_id)
        
        # Visar den uppdaterade listan.
        view_products(products)

    elif choice == '4':
        os.system('cls')
        view_products(products)
        product_id = int(input("Ange ID för produkten som ska ändras: "))
        edit_product(products, "db_products.csv", product_id)
        
        # Visar den uppdaterade listan.
        view_products(products)

    else:
        print("Ogiltigt val, försök igen.")