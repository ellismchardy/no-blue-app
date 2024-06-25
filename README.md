# Blue Light Filter

A simple GUI tool for adjusting screen gamma to reduce blue light emissions on Linux.

## Features
- Adjust screen gamma for red, green, and blue channels.
- Apply settings instantly with sliders or enter specific values.
- Revert to default gamma settings with one click.

## Requirements
- Python 3
- `tkinter` (usually included with Python)
- `xrandr` (for gamma adjustment on Linux)

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/ellismchardy/no-blue-app.git
    cd blue_light_filter
    ```

2. **Install dependencies:**
    ```bash
    sudo apt-get install xrandr python3-tk
    ```

3. **Run the application:**
    ```bash
    python3 no-blue-app.py
    ```

## Usage
- Adjust gamma settings using sliders or by typing values directly into the entry boxes.
- Click "Apply Gamma Settings" to apply the current gamma values to the screen.
- Click "Revert to Defaults" to reset gamma values to 1.0:1.0:1.0 instantly.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
