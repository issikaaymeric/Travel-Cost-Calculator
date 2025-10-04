import openpyxl
import pandas as pd
import tkinter as tk
from tkinter import *


m = tk.Tk() # main window
m.geometry("600x500") # the width and height of the window
m.title("Total Cost Calculation") # title of the window

# Scrollbar
scrollbar = Scrollbar(m)
scrollbar.pack(side=RIGHT, fill=Y)
mylist = Listbox(m, yscrollcommand=scrollbar.set, width=180, height=15)
mylist.pack(pady=10)

# Load the datasets
cities_datasets = pd.read_excel("datasets/cities_datasets.xlsx", engine='openpyxl')
cars_datasets = pd.read_csv("datasets/car_models_dataset.csv", encoding="utf-8")
fuel_price = {"Petrol": 830, "Diesel": 675}

Label(m, text="Select your destination city : ").pack(pady=5)
city_var = StringVar()
city_dropdown = OptionMenu(m, city_var, *cities_datasets['City'].values)
city_dropdown.pack(pady=5)

Label(m, text="Select your car model : ").pack(pady=5)
car_var = StringVar()
car_dropdown = OptionMenu(m, car_var, *cars_datasets['Model'].values)
car_dropdown.pack(pady=5)

Label(m, text="Select your fuel type : ").pack(pady=5)
fuel_var = StringVar()
fuel_dropdown = OptionMenu(m, fuel_var, *fuel_price.keys())
fuel_dropdown.pack(pady=5)


def calculate_cost():
    city = city_var.get()
    car = car_var.get()
    fuel = fuel_var.get()

    if city not in cities_datasets['City'].values or car not in cars_datasets['Model'].values or fuel not in fuel_price:
        Label(m, text="Invalid input. Please check your entries and try again.").pack(pady=20)
        return # to exit the function if input is invalid

    # Get the distance for the selected city
    distance = cities_datasets.loc[cities_datasets['City'] == city, 'Distance_km'].values[0]

    # Get the fuel consumption for the selected car
    fuel_consumption = cars_datasets.loc[cars_datasets['Model'] == car, 'Consumption L/100km'].values[0]

    # Get the price per liter for the selected fuel type
    price_per_liter = fuel_price[fuel]

    # Calculate total cost
    total_fuel_needed = (fuel_consumption / 100) * distance
    total_cost = total_fuel_needed * price_per_liter

    # Display the result
    mylist.insert(END, "Summary:")
    mylist.insert(END, f"Destination City: {city} ({distance} km)")
    mylist.insert(END, f"Car: {car} ({fuel_consumption} L/100km)")
    mylist.insert(END, f"Fuel Type: {fuel} ({price_per_liter} CFA/L)")
    mylist.insert(END, f"Fuel Needed: {total_fuel_needed:.2f} L")
    mylist.insert(END, f"Total Cost: {total_cost:.0f} CFA")
    mylist.insert(END, "")  # blank line for spacing
    mylist.yview_moveto(1)
calculate_button = tk.Button(m, text="Calculate Cost", command=calculate_cost, bg="green", fg="white").pack(pady=5)

def clear_list():
    mylist.delete(0, END)
clear_button = tk.Button(m, text="Clear", command=clear_list, bg="lightgray").pack(pady=5)

def exit_app():
    m.destroy()
exit_button = tk.Button(m, text="Exit", command=exit_app, bg="red", fg="white").pack(pady=5)

m.mainloop() # keep the window open