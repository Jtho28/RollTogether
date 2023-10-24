import tkinter as tk

class RideSharingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ride Sharing App")

        self.profile_button = tk.Button(root, text="Profile", command=self.profile_menu)
        self.profile_button.pack()

        self.view_rides_button = tk.Button(root, text="View Rides", command=self.view_rides_menu)
        self.view_rides_button.pack()

        self.manage_rides_button = tk.Button(root, text="Manage Rides", command=self.manage_rides_menu)
        self.manage_rides_button.pack()

    def profile_menu(self):
        profile_window = tk.Toplevel(self.root)
        profile_window.title("Profile")
        # Add profile menu widgets here

    def view_rides_menu(self):
        view_rides_window = tk.Toplevel(self.root)
        view_rides_window.title("View Rides")
        # Add view rides menu widgets here

    def manage_rides_menu(self):
        manage_rides_window = tk.Toplevel(self.root)
        manage_rides_window.title("Manage Rides")
        # Add manage rides menu widgets here

if __name__ == "__main__":
    root = tk.Tk()
    app = RideSharingApp(root)
    root.mainloop()
