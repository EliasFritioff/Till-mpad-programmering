def create_list(cars):

    return "\n".join([f"{i+1}) {cars}" for i, cars in enumerate(cars)])

cars = ["Porsche 911 Turbo S",
        "Ferrari LaFerrari",
        "Lamborghini Revuelto"]

print("Här kommer en lista över alla existerande bilar!")
print("\n")
print (create_list(cars))