import tkinter as tk
from tkinter import messagebox

def add_rider():
    rider_name = rider_name_entry.get()
    rider_contact_info = rider_contact_info_entry.get()
    messagebox.showinfo("Success", f"Rider {rider_name} added!")

def add_driver():
    driver_name = driver_name_entry.get()
    driver_contact_info = driver_contact_info_entry.get()
    vehicle_make = vehicle_make_entry.get()
    vehicle_model = vehicle_model_entry.get()
    vehicle_plate = vehicle_plate_entry.get()
    messagebox.showinfo("Success", f"Driver {driver_name} added with {vehicle_make} - {vehicle_model} ({vehicle_plate})")

def request_ride():
    rider_request = rider_request_entry.get()
    messagebox.showinfo("Request Received", f"Ride request: {rider_request}")

def post_ride():
    driver_post = driver_post_entry.get()
    messagebox.showinfo("Ride Posted", f"Ride post: {driver_post}")

def main():
    root = tk.Tk()
    root.title("Ride Sharing Platform")

    root.geometry("500x400")

    # Riders Tab
    riders_tab = tk.Frame(root)
    riders_tab.pack(fill='both', expand=1)

    rider_frame = tk.LabelFrame(riders_tab, text="Add Rider")
    rider_frame.pack(padx=10, pady=10)

    tk.Label(rider_frame, text="Rider Name:").grid(row=0, column=0)
    rider_name_entry = tk.Entry(rider_frame)
    rider_name_entry.grid(row=0, column=1)

    tk.Label(rider_frame, text="Contact Info:").grid(row=1, column=0)
    rider_contact_info_entry = tk.Entry(rider_frame)
    rider_contact_info_entry.grid(row=1, column=1)

    add_rider_button = tk.Button(rider_frame, text="Add Rider", command=add_rider)
    add_rider_button.grid(row=2, columnspan=2)

    rider_request_frame = tk.LabelFrame(riders_tab, text="Rider Request Ride")
    rider_request_frame.pack(padx=10, pady=10)

    tk.Label(rider_request_frame, text="Request:").grid(row=0, column=0)
    rider_request_entry = tk.Entry(rider_request_frame)
    rider_request_entry.grid(row=0, column=1)

    request_button = tk.Button(rider_request_frame, text="Request Ride", command=request_ride)
    request_button.grid(row=1, columnspan=2)

    # Drivers Tab
    drivers_tab = tk.Frame(root)
    drivers_tab.pack(fill='both', expand=1)

    driver_frame = tk.LabelFrame(drivers_tab, text="Add Driver")
    driver_frame.pack(padx=10, pady=10)

    tk.Label(driver_frame, text="Driver Name:").grid(row=0, column=0)
    driver_name_entry = tk.Entry(driver_frame)
    driver_name_entry.grid(row=0, column=1)

    tk.Label(driver_frame, text="Contact Info:").grid(row=1, column=0)
    driver_contact_info_entry = tk.Entry(driver_frame)
    driver_contact_info_entry.grid(row=1, column=1)

    tk.Label(driver_frame, text="Vehicle Make:").grid(row=2, column=0)
    vehicle_make_entry = tk.Entry(driver_frame)
    vehicle_make_entry.grid(row=2, column=1)

    tk.Label(driver_frame, text="Vehicle Model:").grid(row=3, column=0)
    vehicle_model_entry = tk.Entry(driver_frame)
    vehicle_model_entry.grid(row=3, column=1)

    tk.Label(driver_frame, text="Vehicle Plate:").grid(row=4, column=0)
    vehicle_plate_entry = tk.Entry(driver_frame)
    vehicle_plate_entry.grid(row=4, column=1)

    add_driver_button = tk.Button(driver_frame, text="Add Driver", command=add_driver)
    add_driver_button.grid(row=5, columnspan=2)

    driver_post_frame = tk.LabelFrame(drivers_tab, text="Driver Post Ride")
    driver_post_frame.pack(padx=10, pady=10)

    tk.Label(driver_post_frame, text="Post:").grid(row=0, column=0)
    driver_post_entry = tk.Entry(driver_post_frame)
    driver_post_entry.grid(row=0, column=1)

    post_button = tk.Button(driver_post_frame, text="Post Ride", command=post_ride)
    post_button.grid(row=1, columnspan=2)

    root.mainloop()

if __name__ == "__main__":
    main()
