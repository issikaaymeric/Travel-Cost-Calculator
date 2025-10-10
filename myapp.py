import customtkinter as ctk
import pandas as pd

main_window = ctk.CTk()
main_window.geometry("600x500")
main_window.title("Total Cost Calculation")

# Scrollbar and Textbox
scrollbar = ctk.CTkScrollbar(main_window)
scrollbar.pack(side="right", fill="y")

mylist = ctk.CTkTextbox(main_window, width=500, height=200, yscrollcommand=scrollbar.set)
mylist.pack(pady=10)
mylist.configure(state="disabled")
scrollbar.configure(command=mylist.yview)

# Load the datasets
cities_datasets = pd.read_excel("datasets/cities_datasets.xlsx", engine='openpyxl')
cars_datasets = pd.read_csv("datasets/car_models_dataset.csv", encoding="utf-8")
fuel_price = {"Petrol": 830, "Diesel": 675}

# City Dropdown
ctk.CTkLabel(main_window, text="Select your destination city from Abidjan:").pack(pady=5)
city_var = ctk.StringVar()
city_dropdown = ctk.CTkOptionMenu(main_window, variable=city_var, values=cities_datasets['City'].values.tolist())
city_dropdown.pack(pady=5)

# Car Dropdown
ctk.CTkLabel(main_window, text="Select your car model:").pack(pady=5)
car_var = ctk.StringVar()
car_dropdown = ctk.CTkOptionMenu(main_window, variable=car_var, values=cars_datasets['Full Model'].values.tolist())
car_dropdown.pack(pady=5)

# Fuel Dropdown
ctk.CTkLabel(main_window, text="Select your fuel type:").pack(pady=5)
fuel_var = ctk.StringVar()
fuel_dropdown = ctk.CTkOptionMenu(main_window, variable=fuel_var, values=list(fuel_price.keys()))
fuel_dropdown.pack(pady=5)

# Result label for errors
result_label = ctk.CTkLabel(main_window, text="")
result_label.pack(pady=5)

# Calculation function
def calculate_cost():
    city = city_var.get()
    car = car_var.get()
    fuel = fuel_var.get()

    if city not in cities_datasets['City'].values or car not in cars_datasets['Full Model'].values or fuel not in fuel_price:
        result_label.configure(text="Invalid input. Please check your entries.")
        return
    else:
        result_label.configure(text="")

    distance = cities_datasets.loc[cities_datasets['City'] == city, 'Distance_km'].values[0]
    fuel_consumption = cars_datasets.loc[cars_datasets['Full Model'] == car, 'Consumption L/100km'].values[0]
    price_per_liter = fuel_price[fuel]

    total_fuel_needed = (fuel_consumption / 100) * distance
    total_cost = total_fuel_needed * price_per_liter

    mylist.configure(state="normal")
    mylist.insert("end", f"Summary:\n")
    mylist.insert("end", f"Destination City: {city} ({distance} km)\n")
    mylist.insert("end", f"Car: {car} ({fuel_consumption} L/100km)\n")
    mylist.insert("end", f"Fuel Type: {fuel} ({price_per_liter} CFA/L)\n")
    mylist.insert("end", f"Fuel Needed: {total_fuel_needed:.2f} L\n")
    mylist.insert("end", f"Total Cost: {total_cost:.0f} CFA\n\n")
    mylist.configure(state="disabled")
    mylist.yview_moveto(1)

# Calculation Button
ctk.CTkButton(main_window, text="Calculate Cost", command=calculate_cost, fg_color="green", text_color="white").pack(pady=5)

# Delete button
def clear_result():
    mylist.configure(state="normal")
    mylist.delete("1.0", "end")
    mylist.configure(state="disabled")

ctk.CTkButton(main_window, text="Clear", command=clear_result, fg_color="gray").pack(pady=5)

# Exit button
def exit_app():
    main_window.destroy()

ctk.CTkButton(main_window, text="Exit", command=exit_app, fg_color="red", text_color="white").pack(pady=5)

main_window.mainloop()
