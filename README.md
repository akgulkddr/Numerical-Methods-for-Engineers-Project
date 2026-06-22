# Agricultural Irrigation Optimization Simulation

This project is a web application developed with Flask. The user can start a 30-day accelerated field simulation by entering parameters such as crop type, temperature, irrigation frequency, irrigation amount, and fertilizer amount.

## Features
- Crop type selection (tomato, pepper, cucumber, corn, wheat)
- Input for temperature, irrigation frequency, irrigation amount, and fertilizer amount
- 30-day accelerated simulation (in 30 seconds)
- Field grid and crop images according to growth stages
- Day information shown when clicking any crop cell
- Side panel with selected crop name and image
- "Planting completed" message at the end of the simulation

## Installation
1. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
2. Start the application:
   ```
   python app.py
   ```
3. Open your browser and go to `http://127.0.0.1:5000`.

## Note
You can add sample images to the `static` folder for crops. Currently, placeholder images are used.
