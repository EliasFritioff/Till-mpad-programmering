class Car:
    def __init__(self):
        self.car_list = []  # Använder en lista för att hålla ordningen på bilarna

    def add_car(self, make, model):
        self.car_list.append((make, model))  # Lägg till bilen som ett par (make, model)

    def list_cars(self):
        for i, (make, model) in enumerate(self.car_list, 1):
            print(f"{i}) {make} - {model}")

car = Car()

car.add_car("Audi", "R8")
car.add_car("Lamborghini", "Gallardo")
car.add_car("Toyota", "Brz")
car.add_car("Honda", "Civic")
car.add_car("Mazda", "Mx5")
car.add_car("Ferrari", "F40")
car.add_car("Ferrari", "LaFerrari")

car.list_cars()