'''
MAIN.PY: python programm som skriver ut en lista och redigerar csv filen db_inventory.csv

__author__  = "Elias Fritioff"
__version__ = "1.0.7"
__email__   = "Elias.Fritioff@elev.ga.ntig.se"
'''

import csv
import os
import locale
import uuid
from tabulate import tabulate
from colorama import Fore, Back, Style, init
init()  # Initierar colorama

def load_data(filename): 
    products = []
    with open(filename, 'r', encoding='utf-8') as file:  # la till utf-8 eftersom att å,ä,ö inte fungerade i terminalen utan.
        reader = csv.DictReader(file)
        for row in reader:
            id = row['id']  
            name = row['name']
            desc = row['desc']
            price = float(row['price'])
            quantity = int(row['quantity'])
            
            # Lägger till en ny produkt i listan products som en dictionary
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

# Funktion för att spara data till csv filen db_inventory.csv
def save_data(filename, products):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        fieldnames = ['id', 'name', 'desc', 'price', 'quantity']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        
        # Skriver varje produkt i filen
        for product in products:
            writer.writerow(product)

# Funktion för att formatera beskrivningen av produkten
def format_description(desc, max_length=70):
    if len(desc) > max_length:
        return desc[:max_length] + "..."
    return desc

# Funktion för att hämta produkter i tabellformat
def get_products(products): 
    product_list = []
    for index, product in enumerate(products):
        short_desc = format_description(product['desc'])
        product_info = [index + 1, product['name'], short_desc, f"{product['price']} kr", f"{product['quantity']} st"]
        product_list.append(product_info)
    
    return tabulate(product_list, headers=["Nummer", "Namn", "Beskrivning", "Pris", "Antal"], tablefmt="grid")

# Funktion för att hämta en produkt från ett ID
def get_product_by_id(products, product_number): 
    for product in products:
        if product['id'] == product_number:
           return f"UUID: {product['id']}\nNamn: {product['name']}\nBeskrivning: {product['desc']}\nPris: {product['price']} kr\nAntal: {product['quantity']} st"
    return "Product not found."

# Funktion för att lägga till en produkt samt skapa ett uuid till produkten
def add_product(products, filename, name, desc, price, quantity):
    new_id = str(uuid.uuid4())
    
    new_product = {
        "id": new_id,
        "name": name,
        "desc": desc,
        "price": price,
        "quantity": quantity
    }
    
    products.append(new_product)
    save_data(filename, products)
    
    print(f"Produkten '{name}' har lagts till med ID {new_id}.")

# Funktion för att ta bort en produkt
def remove_product(products, filename, product_number):
    # Kontrollera om produktnumret är inom listans index
    if 0 <= product_number < len(products):
        product = products[product_number]
        products.remove(product)
        save_data(filename, products)
        print(Fore.RED + f"Produkten med nummer {product_number + 1} har tagits bort." + Style.RESET_ALL)  # Lägg till 1 för att visa rätt nummer
    else:
        print(Fore.RED + f"Produkten med nummer {product_number + 1} hittades inte." + Style.RESET_ALL)  # Lägg till 1 för att visa rätt nummer

# Kollar i listan products för att se om id matchar för att sedan kunna redigera
def edit_product(products, filename, product_number):
    for product in products:
        if product['id'] == product_number:
            print(f"Redigerar produkt med nummer {product_number}:")
            new_name = input(f"Ange nytt namn för {product['name']} (tryck Enter för att behålla): ") or product['name']
            new_desc = input(f"Ange ny beskrivning för {product['desc']} (tryck Enter för att behålla): ") or product['desc']
            new_price = input(f"Ange nytt pris för {product['price']} (tryck Enter för att behålla): ")
            new_price = float(new_price) if new_price else product['price']
            new_quantity = input(f"Ange nytt antal för {product['quantity']} (tryck Enter för att behålla): ")
            new_quantity = int(new_quantity) if new_quantity else product['quantity']
            
            # Alla nya värden som användaren skrivit in
            product['name'] = new_name
            product['desc'] = new_desc
            product['price'] = new_price
            product['quantity'] = new_quantity
            
            # Värderna i products uppdateras
            save_data(filename, products)
            print(f"Produkten med nummer {product_number} har uppdaterats.")
            return
    print(f"Produkten med nummer {product_number} hittades inte.")

def menu():  # Använder colorama för att få menyn att ändra färg och mer (Fore, Back & Style)
    print("\n" + Back.BLUE + Fore.WHITE + Style.BRIGHT + "--- MENY ---" + Style.RESET_ALL)
    print(Back.RESET + Fore.WHITE + Style.BRIGHT + "1. " + Fore.CYAN + "Visa produkter" + Style.RESET_ALL)
    print(Back.RESET + Fore.WHITE + Style.BRIGHT + "2. " + Fore.GREEN + "Lägg till produkt" + Style.RESET_ALL)
    print(Back.RESET + Fore.WHITE + Style.BRIGHT + "3. " + Fore.RED + "Ta bort produkt" + Style.RESET_ALL)
    print(Back.RESET + Fore.WHITE + Style.BRIGHT + "4. " + Fore.MAGENTA + "Ändra produkt" + Style.RESET_ALL)
    print(Back.RESET + Fore.WHITE + Style.BRIGHT + "5. " + Fore.YELLOW + "Visa specifik produkt" + Style.RESET_ALL)
    print(Back.RESET + Fore.WHITE + Style.BRIGHT + "6. " + Fore.BLUE + "Visa upp produktvärde" + Style.RESET_ALL)
    print(Back.RESET + Fore.WHITE + Style.BRIGHT + "7. " + Fore.RED + "Stäng ner program" + Style.RESET_ALL)
    return input(Fore.CYAN + Style.BRIGHT + "\nVälj ett alternativ (1-7): " + Style.RESET_ALL)

# Funktionen för att visa upp products
def view_products(products):
    print(get_products(products))

# Funktionen för att visa detaljer hos en specifik produkt
def view_specific_product(products):
    try:
        product_number = int(input("Ange produktens nummer för att visa detaljer: ")) - 1
        if 0 <= product_number < len(products):
            os.system('cls')
            product = products[product_number]
            print(get_product_by_id(products, product['id']))
        else:  # Felmeddelande om produktnumret är ogiltigt
            print(Fore.RED + "Ogiltigt produktnummer." + Style.RESET_ALL)
    except ValueError:  # Felmeddelande om användaren inte skriv in ett giltigt nummer
        print("Vänligen ange ett giltigt nummer.")

# Skapar variabeln products som laddar in produktdata från vår db_inventory.csv fil
products = load_data("db_inventory.csv")
os.system('cls')
view_products(products)  # visar products när jag startar programmet

# Main loop för att visa upp menyn
while True:
    choice = menu()

    # Menyval 1 = Visa Produkter
    if choice == '1':
        os.system('cls')
        view_products(products)

# Menyval 2 = Lägg till produkt
    elif choice == '2':
        os.system('cls')
        view_products(products)

        new_product_name = input('Ange den nya produktens namn: ')
        new_product_desc = input(f"Ange en ny beskrivning för {new_product_name}: ")

    # Felhantering för pris
        while True:
            try:
                new_product_price = float(input(f"Ange ett pris för {new_product_name}: "))
                break  # Om priset är ett giltigt så bryts loopen
            except ValueError:
                print(Fore.RED + "Vänligen ange ett giltigt pris (ett nummer)." + Style.RESET_ALL)

        # Felhantering för antal
        while True:
            try:
                new_product_quantity = int(input(f"Ange hur många {new_product_name} som existerar: "))
                break  # Om antalet är ett giltigt heltal, bryt loopen
            except ValueError:
                print(Fore.RED + "Vänligen ange ett giltigt antal (ett heltal)." + Style.RESET_ALL)

        add_product(products, "db_inventory.csv", new_product_name, new_product_desc, new_product_price, new_product_quantity)

        view_products(products)


    # Menyval 3 = Ta bort produkt
    elif choice == '3':
        os.system('cls')
        view_products(products)
        try:
            product_number = int(input("Ange nummer för produkten som ska tas bort: ")) - 1  # Användarens produktnummer justeras till index
            remove_product(products, "db_inventory.csv", product_number)
            view_products(products)  # Visar uppdaterad produktlista efter borttagning
        except ValueError:
            print(Fore.RED + "Ogiltigt produktnummer." + Style.RESET_ALL)

    # Menyval 4 = Ändra produkt
    elif choice == '4':
        os.system('cls')
        view_products(products)
        product_number = input("Ange nummer för produkten som ska ändras: ")
        edit_product(products, "db_inventory.csv", product_number)

        view_products(products)

    # Menyval 5 = Visa specifik produkt
    elif choice == '5':
        os.system('cls')
        view_products(products)
        view_specific_product(products)

    # Menyval 6 = Visa upp produktvärde
    elif choice == '6':
        os.system('cls')
        total_value = 0  # För att hålla reda på det totala värdet av alla produkterna
        print(Fore.BLUE + Style.BRIGHT + "--- Värde av produkter ---" + Style.RESET_ALL)

        for product in products:
            product_value = round(product['price'] * product['quantity'], 1)  # Avrundar till en decimal
            total_value += product_value
            print(Fore.WHITE + Style.BRIGHT + f"{product['name']}," + Style.RESET_ALL + Fore.BLUE + Style.BRIGHT + f" Totalt värde: {product_value} kr" + Style.RESET_ALL)

        total_value = round(total_value, 1)  # Avrunda det totala värdet till en decimal
        print(Back.WHITE + Fore.BLACK+ f"\nTotalt värde av alla produkter: {total_value} kr" + Style.RESET_ALL)

    # menyval 7 = stänger ner programmet.5
    elif choice == '7':
        os.system('cls')
        print(Fore.RED + "Programmet avslutas." + Style.RESET_ALL)
        break
    else:
        print(Fore.RED + "Ogiltigt val, försök igen." + Style.RESET_ALL) # meny val utöver 1-7 är ogiltiga