import datetime
from abc import ABC, abstractmethod

class Vehicle(ABC):
    def __init__(self, vehicle_id, model, year, color, price_per_day):
        self.vehicle_id = vehicle_id
        self.model = model
        self.year = year
        self.color = color
        self.price_per_day = price_per_day
        self.is_available = True
    
    @abstractmethod
    def display_details(self):
        pass
    
    def rent(self):
        if self.is_available:
            self.is_available = False
            return True
        return False
    
    def return_vehicle(self):
        self.is_available = True

class Car(Vehicle):
    def __init__(self, vehicle_id, model, year, color, price_per_day, num_seats, fuel_type):
        super().__init__(vehicle_id, model, year, color, price_per_day)
        self.num_seats = num_seats
        self.fuel_type = fuel_type
        self.vehicle_type = "Car"
    
    def display_details(self):
        return (f"Car ID: {self.vehicle_id}\nModel: {self.model}\nYear: {self.year}\n"
                f"Color: {self.color}\nSeats: {self.num_seats}\nFuel Type: {self.fuel_type}\n"
                f"Price per day: ${self.price_per_day}\nAvailable: {'Yes' if self.is_available else 'No'}")

class Bike(Vehicle):
    def __init__(self, vehicle_id, model, year, color, price_per_day, bike_type, engine_cc):
        super().__init__(vehicle_id, model, year, color, price_per_day)
        self.bike_type = bike_type
        self.engine_cc = engine_cc
        self.vehicle_type = "Bike"
    
    def display_details(self):
        return (f"Bike ID: {self.vehicle_id}\nModel: {self.model}\nYear: {self.year}\n"
                f"Color: {self.color}\nType: {self.bike_type}\nEngine: {self.engine_cc}cc\n"
                f"Price per day: ${self.price_per_day}\nAvailable: {'Yes' if self.is_available else 'No'}")

class Customer:
    def __init__(self, customer_id, name, email, phone):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.phone = phone
    
    def display_details(self):
        return f"Customer ID: {self.customer_id}\nName: {self.name}\nEmail: {self.email}\nPhone: {self.phone}"

class Rental:
    def __init__(self, rental_id, vehicle, customer, rental_days):
        self.rental_id = rental_id
        self.vehicle = vehicle
        self.customer = customer
        self.rental_date = datetime.datetime.now()
        self.return_date = None
        self.rental_days = rental_days
        self.total_cost = vehicle.price_per_day * rental_days
        self.is_returned = False
    
    def return_rental(self):
        self.return_date = datetime.datetime.now()
        self.is_returned = True
        self.vehicle.return_vehicle()
        return self.total_cost
    
    def display_details(self):
        return (f"Rental ID: {self.rental_id}\n"
                f"Vehicle: {self.vehicle.model} ({self.vehicle.vehicle_type})\n"
                f"Customer: {self.customer.name}\n"
                f"Rental Date: {self.rental_date.strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"Rental Days: {self.rental_days}\n"
                f"Total Cost: ${self.total_cost}\n"
                f"Returned: {'Yes' if self.is_returned else 'No'}")

class RentalSystem:
    def __init__(self):
        self.vehicles = []
        self.customers = []
        self.rentals = []
        self.next_vehicle_id = 1
        self.next_customer_id = 1
        self.next_rental_id = 1
    
    def add_vehicle(self, vehicle_type, model, year, color, price_per_day, **kwargs):
        if vehicle_type.lower() == "car":
            vehicle = Car(self.next_vehicle_id, model, year, color, price_per_day, 
                          kwargs.get('num_seats', 4), kwargs.get('fuel_type', 'Petrol'))
        elif vehicle_type.lower() == "bike":
            vehicle = Bike(self.next_vehicle_id, model, year, color, price_per_day,
                           kwargs.get('bike_type', 'Standard'), kwargs.get('engine_cc', 150))
        else:
            return None
        
        self.vehicles.append(vehicle)
        self.next_vehicle_id += 1
        return vehicle
    
    def add_customer(self, name, email, phone):
        customer = Customer(self.next_customer_id, name, email, phone)
        self.customers.append(customer)
        self.next_customer_id += 1
        return customer
    
    def find_available_vehicles(self, vehicle_type=None):
        if vehicle_type:
            return [v for v in self.vehicles if v.is_available and v.vehicle_type.lower() == vehicle_type.lower()]
        return [v for v in self.vehicles if v.is_available]
    
    def rent_vehicle(self, vehicle_id, customer_id, rental_days):
        vehicle = next((v for v in self.vehicles if v.vehicle_id == vehicle_id), None)
        customer = next((c for c in self.customers if c.customer_id == customer_id), None)
        
        if not vehicle or not customer:
            return None
        
        if not vehicle.is_available:
            return None
        
        rental = Rental(self.next_rental_id, vehicle, customer, rental_days)
        if vehicle.rent():
            self.rentals.append(rental)
            self.next_rental_id += 1
            return rental
        return None
    
    def return_vehicle(self, rental_id):
        rental = next((r for r in self.rentals if r.rental_id == rental_id and not r.is_returned), None)
        if rental:
            total_cost = rental.return_rental()
            return total_cost
        return None
    
    def display_all_vehicles(self):
        for vehicle in self.vehicles:
            print(vehicle.display_details())
            print("-" * 40)
    
    def display_all_customers(self):
        for customer in self.customers:
            print(customer.display_details())
            print("-" * 40)
    
    def display_all_rentals(self):
        for rental in self.rentals:
            print(rental.display_details())
            print("-" * 40)

def main_menu():
    print("\nVehicle Rental System")
    print("1. Add Vehicle")
    print("2. Add Customer")
    print("3. Rent Vehicle")
    print("4. Return Vehicle")
    print("5. View All Vehicles")
    print("6. View All Customers")
    print("7. View All Rentals")
    print("8. Exit")

def add_vehicle_menu(rental_system):
    print("\nAdd Vehicle")
    vehicle_type = input("Enter vehicle type (Car/Bike): ")
    model = input("Enter model: ")
    year = input("Enter year: ")
    color = input("Enter color: ")
    price_per_day = float(input("Enter price per day: "))
    
    if vehicle_type.lower() == "car":
        num_seats = int(input("Enter number of seats: "))
        fuel_type = input("Enter fuel type: ")
        vehicle = rental_system.add_vehicle(vehicle_type, model, year, color, price_per_day, 
                                          num_seats=num_seats, fuel_type=fuel_type)
    elif vehicle_type.lower() == "bike":
        bike_type = input("Enter bike type: ")
        engine_cc = int(input("Enter engine CC: "))
        vehicle = rental_system.add_vehicle(vehicle_type, model, year, color, price_per_day,
                                          bike_type=bike_type, engine_cc=engine_cc)
    else:
        print("Invalid vehicle type!")
        return
    
    if vehicle:
        print(f"\nVehicle added successfully:\n{vehicle.display_details()}")
    else:
        print("Failed to add vehicle.")

def add_customer_menu(rental_system):
    print("\nAdd Customer")
    name = input("Enter name: ")
    email = input("Enter email: ")
    phone = input("Enter phone: ")
    
    customer = rental_system.add_customer(name, email, phone)
    print(f"\nCustomer added successfully:\n{customer.display_details()}")

def rent_vehicle_menu(rental_system):
    print("\nRent Vehicle")
    print("Available Vehicles:")
    available_vehicles = rental_system.find_available_vehicles()
    if not available_vehicles:
        print("No vehicles available for rent.")
        return
    
    for vehicle in available_vehicles:
        print(f"{vehicle.vehicle_id}: {vehicle.model} ({vehicle.vehicle_type}) - ${vehicle.price_per_day}/day")
    
    vehicle_id = int(input("\nEnter vehicle ID to rent: "))
    customer_id = int(input("Enter customer ID: "))
    rental_days = int(input("Enter number of rental days: "))
    
    rental = rental_system.rent_vehicle(vehicle_id, customer_id, rental_days)
    if rental:
        print(f"\nVehicle rented successfully:\n{rental.display_details()}")
    else:
        print("Failed to rent vehicle. It may be already rented or invalid ID.")

def return_vehicle_menu(rental_system):
    print("\nReturn Vehicle")
    active_rentals = [r for r in rental_system.rentals if not r.is_returned]
    if not active_rentals:
        print("No active rentals to return.")
        return
    
    print("Active Rentals:")
    for rental in active_rentals:
        print(f"{rental.rental_id}: {rental.customer.name} rented {rental.vehicle.model} for {rental.rental_days} days")
    
    rental_id = int(input("\nEnter rental ID to return: "))
    total_cost = rental_system.return_vehicle(rental_id)
    if total_cost is not None:
        print(f"\nVehicle returned successfully. Total cost: ${total_cost}")
    else:
        print("Failed to return vehicle. Invalid rental ID or already returned.")

def main():
    rental_system = RentalSystem()
    
    # Add some sample data
    rental_system.add_vehicle("Car", "Toyota Camry", 2020, "Silver", 5000, num_seats=5, fuel_type="Petrol")
    rental_system.add_vehicle("Car", "Honda Civic", 2021, "Black", 4500, num_seats=5, fuel_type="Petrol")
    rental_system.add_vehicle("Bike", "Yamaha MT-15", 2022, "Blue", 250, bike_type="Sports", engine_cc=155)
    rental_system.add_vehicle("Bike", "Royal Enfield Classic 350", 2021, "Red", 300, bike_type="Cruiser", engine_cc=350)
    rental_system.add_vehicle("Bike", "Royal Enfield continental GT 650", 2021, "Red", 600, bike_type="Cafe Racer", engine_cc=650)
    rental_system.add_vehicle("Car", "Pagani Utopia", 2021, "Purple carbonfiber", 50000, num_seats=2, fuel_type="Petrol")
    rental_system.add_vehicle("Car", "RollsRoyce Cullianan", 2021, "British racing green", 30000, num_seats=5, fuel_type="Petrol")
    
    rental_system.add_customer("Nitish Sir", "Nitish@gmail.com", "5151521515")
    rental_system.add_customer("Vinay Yadav", "vinay@gmail.com", "2551344548")
    rental_system.add_customer("Piyush Kataria", "piyush@gmail.com", "785454654")
    rental_system.add_customer("Manan", "Manan@gmail.com", "1626554659")
    rental_system.add_customer("ashish", "ashish@gmail.com", "874665659")
    
    while True:
        main_menu()
        choice = input("\nEnter your choice (1-8): ")
        
        if choice == "1":
            add_vehicle_menu(rental_system)
        elif choice == "2":
            add_customer_menu(rental_system)
        elif choice == "3":
            rent_vehicle_menu(rental_system)
        elif choice == "4":
            return_vehicle_menu(rental_system)
        elif choice == "5":
            print("\nAll Vehicles:")
            rental_system.display_all_vehicles()
        elif choice == "6":
            print("\nAll Customers:")
            rental_system.display_all_customers()
        elif choice == "7":
            print("\nAll Rentals:")
            rental_system.display_all_rentals()
        elif choice == "8":
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
    