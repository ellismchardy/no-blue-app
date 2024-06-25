import tkinter as tk
from tkinter import Scale, Label, Entry, Button, HORIZONTAL, messagebox
import subprocess
import re

# Function to get the output name of the connected display
def get_output_name():
    result = subprocess.run(['xrandr'], stdout=subprocess.PIPE)
    output = result.stdout.decode()
    match = re.search(r'(\S+) connected', output)
    if match:
        return match.group(1)
    else:
        raise Exception("No connected display found")

# Function to set the gamma values directly
def set_gamma(output_name, red_gamma, green_gamma, blue_gamma):
    command = f"xrandr --output {output_name} --brightness 1 --gamma {red_gamma:.4f}:{green_gamma:.4f}:{blue_gamma:.4f}"
    subprocess.call(command, shell=True)

# Main class for the GUI application
class BlueLightFilterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Blue Light Filter")

        # Determine the output name and store it in the instance
        try:
            self.output_name = get_output_name()
        except Exception as e:
            self.output_name = None
            print(f"Error: {e}")
            tk.Label(root, text="No connected display found.").pack()
            return

        # Default gamma values
        self.default_red_gamma = 1.0
        self.default_green_gamma = 0.88
        self.default_blue_gamma = 0.76

        # Create a label to provide instructions to the user
        self.label = Label(root, text="Adjust the gamma values")
        self.label.pack()

        # Create entry boxes and scales for gamma adjustment
        self.red_entry = Entry(root)
        self.red_entry.insert(0, f"{self.default_red_gamma:.2f}")
        self.red_entry.pack()

        self.red_scale = Scale(root, from_=0.1, to=1.0, orient=HORIZONTAL, resolution=0.01, label="Red Gamma", command=self.update_gamma)
        self.red_scale.set(self.default_red_gamma)
        self.red_scale.pack()

        self.green_entry = Entry(root)
        self.green_entry.insert(0, f"{self.default_green_gamma:.2f}")
        self.green_entry.pack()

        self.green_scale = Scale(root, from_=0.1, to=1.0, orient=HORIZONTAL, resolution=0.01, label="Green Gamma", command=self.update_gamma)
        self.green_scale.set(self.default_green_gamma)
        self.green_scale.pack()

        self.blue_entry = Entry(root)
        self.blue_entry.insert(0, f"{self.default_blue_gamma:.2f}")
        self.blue_entry.pack()

        self.blue_scale = Scale(root, from_=0.1, to=1.0, orient=HORIZONTAL, resolution=0.01, label="Blue Gamma", command=self.update_gamma)
        self.blue_scale.set(self.default_blue_gamma)
        self.blue_scale.pack()

        # Add a button to apply gamma settings
        self.apply_button = Button(root, text="Apply Gamma Settings", command=self.apply_gamma_settings)
        self.apply_button.pack()

        # Add a button to revert gamma settings
        self.revert_button = Button(root, text="Revert to Defaults", command=self.revert_gamma_settings)
        self.revert_button.pack()

        # Bind Return key to entry boxes for instant update
        self.red_entry.bind('<Return>', lambda event: self.update_from_entry(event, 'red'))
        self.green_entry.bind('<Return>', lambda event: self.update_from_entry(event, 'green'))
        self.blue_entry.bind('<Return>', lambda event: self.update_from_entry(event, 'blue'))

    # Method to update gamma values when scales are adjusted
    def update_gamma(self, value):
        red_gamma = float(self.red_scale.get())
        green_gamma = float(self.green_scale.get())
        blue_gamma = float(self.blue_scale.get())
        
        # Update entry boxes with current scale values
        self.red_entry.delete(0, tk.END)
        self.red_entry.insert(0, f"{red_gamma:.2f}")

        self.green_entry.delete(0, tk.END)
        self.green_entry.insert(0, f"{green_gamma:.2f}")

        self.blue_entry.delete(0, tk.END)
        self.blue_entry.insert(0, f"{blue_gamma:.2f}")

        # Apply gamma settings immediately when scales are adjusted
        if self.output_name:
            set_gamma(self.output_name, red_gamma, green_gamma, blue_gamma)

    # Method to update gamma values from entry box input
    def update_from_entry(self, event, color):
        try:
            if color == 'red':
                red_gamma = float(self.red_entry.get())
                self.red_scale.set(red_gamma)
            elif color == 'green':
                green_gamma = float(self.green_entry.get())
                self.green_scale.set(green_gamma)
            elif color == 'blue':
                blue_gamma = float(self.blue_entry.get())
                self.blue_scale.set(blue_gamma)
            
            # Apply gamma settings immediately from entry box input
            if self.output_name:
                set_gamma(self.output_name, float(self.red_scale.get()), float(self.green_scale.get()), float(self.blue_scale.get()))
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number.")

    # Method to apply gamma settings using entry box values
    def apply_gamma_settings(self):
        try:
            red_gamma = float(self.red_entry.get())
            green_gamma = float(self.green_entry.get())
            blue_gamma = float(self.blue_entry.get())
            
            if self.output_name:
                set_gamma(self.output_name, red_gamma, green_gamma, blue_gamma)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid gamma values.")

    # Method to revert gamma settings to default values
    def revert_gamma_settings(self):
        if self.output_name:
            set_gamma(self.output_name, 1.0, 1.0, 1.0)
            
            # Update scales and entry boxes to reflect default values
            self.red_entry.delete(0, tk.END)
            self.red_entry.insert(0, f"{1.0:.2f}")
            self.red_scale.set(1.0)

            self.green_entry.delete(0, tk.END)
            self.green_entry.insert(0, f"{1.0:.2f}")
            self.green_scale.set(1.0)

            self.blue_entry.delete(0, tk.END)
            self.blue_entry.insert(0, f"{1.0:.2f}")
            self.blue_scale.set(1.0)

# Main function to run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = BlueLightFilterApp(root)
    root.mainloop()
