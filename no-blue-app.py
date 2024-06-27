import tkinter as tk
from tkinter import ttk, messagebox
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

# Function to set the gamma values and brightness directly
def set_gamma_and_brightness(output_name, red_gamma, green_gamma, blue_gamma, brightness):
    command = f"xrandr --output {output_name} --brightness {brightness} --gamma {red_gamma:.4f}:{green_gamma:.4f}:{blue_gamma:.4f}"
    subprocess.call(command, shell=True)

# Main class for the GUI application
class NoBlueApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NoBlueApp - Blue Light Filter")
        self.root.geometry("500x600")  # Set initial window size
        self.root.configure(bg='#f0f0f0')  # Set background color to light gray gradient

        # Determine the output name and store it in the instance
        try:
            self.output_name = get_output_name()
        except Exception as e:
            self.output_name = None
            print(f"Error: {e}")
            ttk.Label(root, text="No connected display found.", foreground='black', background='#f0f0f0').pack(pady=20)
            return

        # Default gamma and brightness values
        self.default_red_gamma = 1.0
        self.default_green_gamma = 0.90
        self.default_blue_gamma = 0.76
        self.default_brightness = 0.70

        # Title label with a bold modern font
        self.title_label = ttk.Label(root, text="NoBlueApp", font=("Helvetica", 25, "bold"), foreground='black', background='#f0f0f0')
        self.title_label.pack(pady=(20, 30))  # Adjust vertical padding

        # Create a label to provide instructions to the user
        self.label = ttk.Label(root, text="Adjust the gamma values and brightness", foreground='black', background='#f0f0f0')
        self.label.pack()

        # Red Gamma Title
        self.red_title = ttk.Label(root, text="Red Gamma", font=("Helvetica", 12, "bold"), foreground='black', background='#f0f0f0')
        self.red_title.pack(pady=(20, 0))  # Adjust vertical padding

        # Create entry box and scale for Red Gamma adjustment
        self.red_entry = ttk.Entry(root, font=('Helvetica', 12))
        self.red_entry.insert(0, f"{self.default_red_gamma:.2f}")
        self.red_entry.pack(pady=(0, 10))  # Adjust vertical spacing

        self.red_scale = ttk.Scale(root, from_=0.1, to=1.0, orient=tk.HORIZONTAL, length=200, style='custom.Horizontal.TScale',
                                   command=self.update_settings)
        self.red_scale.set(self.default_red_gamma)
        self.red_scale.pack()

        # Green Gamma Title
        self.green_title = ttk.Label(root, text="Green Gamma", font=("Helvetica", 12, "bold"), foreground='black', background='#f0f0f0')
        self.green_title.pack(pady=(20, 0))  # Adjust vertical padding

        # Create entry box and scale for Green Gamma adjustment
        self.green_entry = ttk.Entry(root, font=('Helvetica', 12))
        self.green_entry.insert(0, f"{self.default_green_gamma:.2f}")
        self.green_entry.pack(pady=(0, 10))  # Adjust vertical spacing

        self.green_scale = ttk.Scale(root, from_=0.1, to=1.0, orient=tk.HORIZONTAL, length=200, style='custom.Horizontal.TScale',
                                        command=self.update_settings)
        self.green_scale.set(self.default_green_gamma)
        self.green_scale.pack()

        # Blue Gamma Title
        self.blue_title = ttk.Label(root, text="Blue Gamma", font=("Helvetica", 12, "bold"), foreground='black', background='#f0f0f0')
        self.blue_title.pack(pady=(20, 0))  # Adjust vertical padding

        # Create entry box and scale for Blue Gamma adjustment
        self.blue_entry = ttk.Entry(root, font=('Helvetica', 12))
        self.blue_entry.insert(0, f"{self.default_blue_gamma:.2f}")
        self.blue_entry.pack(pady=(0, 10))  # Adjust vertical spacing

        self.blue_scale = ttk.Scale(root, from_=0.1, to=1.0, orient=tk.HORIZONTAL, length=200, style='custom.Horizontal.TScale',
                                    command=self.update_settings)
        self.blue_scale.set(self.default_blue_gamma)
        self.blue_scale.pack()

        # Brightness Title
        self.brightness_title = ttk.Label(root, text="Brightness", font=("Helvetica", 12, "bold"), foreground='black', background='#f0f0f0')
        self.brightness_title.pack(pady=(20, 0))  # Adjust vertical padding

        # Create entry box and scale for Brightness adjustment
        self.brightness_entry = ttk.Entry(root, font=('Helvetica', 12))
        self.brightness_entry.insert(0, f"{self.default_brightness:.2f}")
        self.brightness_entry.pack(pady=(0, 10))  # Adjust vertical spacing

        self.brightness_scale = ttk.Scale(root, from_=0.1, to=1.0, orient=tk.HORIZONTAL, length=200, style='custom.Horizontal.TScale',
                                          command=self.update_settings)
        self.brightness_scale.set(self.default_brightness)
        self.brightness_scale.pack()

        # Add a button to revert gamma settings
        self.revert_button = ttk.Button(root, text="Revert to Defaults", command=self.revert_settings)
        self.revert_button.pack(pady=(20, 30))  # Adjust vertical padding

        # Bind Return key to entry boxes for instant update
        self.red_entry.bind('<Return>', lambda event: self.update_from_entry(event, 'red'))
        if self.output_name:
            self.green_entry.bind('<Return>', lambda event: self.update_from_entry(event, 'green'))
            self.blue_entry.bind('<Return>', lambda event: self.update_from_entry(event, 'blue'))
            self.brightness_entry.bind('<Return>', lambda event: self.update_from_entry(event, 'brightness'))

        # Style configuration for circular sliders
        self.root.style = ttk.Style()
        self.root.style.theme_use('clam')  # Use a consistent theme for ttk widgets
        self.root.style.configure('custom.Horizontal.TScale', sliderthickness=20, troughcolor='#cccccc', background='#cccccc',
                                  foreground='#000000', gripcount=0)  # Adjust slider appearance

    # Method to update gamma values and brightness when scales are adjusted
    def update_settings(self, value):
        red_gamma = float(self.red_scale.get())
        green_gamma = float(self.green_scale.get())
        blue_gamma = float(self.blue_scale.get())
        brightness = float(self.brightness_scale.get())

        # Update entry boxes with current scale values
        self.red_entry.delete(0, tk.END)
        self.red_entry.insert(0, f"{red_gamma:.2f}")

        self.green_entry.delete(0, tk.END)
        self.green_entry.insert(0, f"{green_gamma:.2f}")

        self.blue_entry.delete(0, tk.END)
        self.blue_entry.insert(0, f"{blue_gamma:.2f}")

        self.brightness_entry.delete(0, tk.END)
        self.brightness_entry.insert(0, f"{brightness:.2f}")

        # Apply gamma and brightness settings immediately when scales are adjusted
        if self.output_name:
            set_gamma_and_brightness(self.output_name, red_gamma, green_gamma, blue_gamma, brightness)

    # Method to update gamma values and brightness from entry box input
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
            elif color == 'brightness':
                brightness = float(self.brightness_entry.get())
                self.brightness_scale.set(brightness)

            # Apply gamma and brightness settings immediately from entry box input
            if self.output_name:
                set_gamma_and_brightness(self.output_name, float(self.red_scale.get()), float(self.green_scale.get()),
                          float(self.blue_scale.get()), float(self.brightness_scale.get()))
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number.")

    # Method to revert gamma and brightness settings to default values
    def revert_settings(self):
        if self.output_name:
            set_gamma_and_brightness(self.output_name, 1.0, 1.0, 1.0, 1.0)

            # Update scales and entry boxes to reflect default values
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

            self.brightness_entry.delete(0, tk.END)
            self.brightness_entry.insert(0, f"{1.0:.2f}")
            self.brightness_scale.set(1.0)

# Main function to run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = NoBlueApp(root)
    root.mainloop()
