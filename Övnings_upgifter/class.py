import os

class Car:
    def __init__(self, tillverkare, model, färg):
        self.tillverkare = tillverkare
        self.model = model
        self.färg = färg

    def view_car(self):
        return f"{self.tillverkare} - {self.model} ({self.färg})"

# rensa terminalen med (cls/clear)
os.system("cls")

cars = []

while True:
    tillverkare = input("tillverkare: ")
    model = input("Model: ")
    färg = input("Färg: ")

    # skapa en ny bil med (tillverkare, model, färg)
    cars.append(Car(tillverkare, model, färg))

    # Printa alla bilar som finns i listan
    for car in cars:
        print(car.view_car())