# create_placeholder_images.py
# This script generates simple placeholder images for each crop and growth stage.
# It uses the Pillow library to draw basic representations for tomato, pepper, cucumber, corn, and wheat.

from PIL import Image, ImageDraw, ImageFont  # Import image libraries
import os  # For file and directory operations
from flask import Flask, request, jsonify  # For creating a Flask API
from scipy.optimize import root_scalar  # For root finding

# List of crops and their representative colors
crops = [
    ("domates", "#ff6347"),   # Tomato
    ("biber", "#4caf50"),     # Pepper
    ("salatalik", "#8bc34a"), # Cucumber
    ("misir", "#ffd600"),     # Corn
    ("bugday", "#fbc02d")     # Wheat
]
stages = [1, 2, 3, 4]  # Growth stages

# Image size and output directory
size = (32, 32)
img_dir = "static/img"
os.makedirs(img_dir, exist_ok=True)  # Create directory if it doesn't exist

def draw_domates(stage):
    # Draws a tomato at the given growth stage
    img = Image.new("RGBA", (32, 32), (255, 255, 255, 0))  # Transparent background
    draw = ImageDraw.Draw(img)
    # Stage 1: seed, Stage 2: sprout, Stage 3: growing, Stage 4: mature
    if stage == 1:
        draw.ellipse([12, 16, 20, 24], fill="#ff6347")  # Small tomato
    elif stage == 2:
        draw.ellipse([12, 16, 20, 24], fill="#ff6347")
        draw.line([16, 12, 16, 16], fill="#388e3c", width=2)  # Sprout
    elif stage == 3:
        draw.ellipse([8, 8, 24, 24], fill="#ff6347")  # Bigger tomato
        draw.line([16, 4, 16, 8], fill="#388e3c", width=3)
    else:
        draw.ellipse([6, 6, 26, 26], fill="#ff6347")  # Largest tomato
        draw.line([16, 0, 16, 8], fill="#388e3c", width=4)
        draw.line([16, 4, 12, 8], fill="#388e3c", width=2)
        draw.line([16, 4, 20, 8], fill="#388e3c", width=2)
    return img

def draw_biber(stage):
    # Draws a pepper at the given growth stage
    img = Image.new("RGBA", (32, 32), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    if stage == 1:
        draw.ellipse([14, 18, 18, 22], fill="#4caf50")  # Small pepper
    elif stage == 2:
        draw.ellipse([14, 18, 18, 22], fill="#4caf50")
        draw.line([16, 14, 16, 18], fill="#388e3c", width=2)
    elif stage == 3:
        draw.rectangle([13, 10, 19, 24], fill="#4caf50")
        draw.ellipse([13, 20, 19, 26], fill="#388e3c")
    else:
        draw.rectangle([12, 6, 20, 26], fill="#4caf50")
        draw.ellipse([12, 22, 20, 28], fill="#388e3c")
        draw.line([16, 2, 16, 6], fill="#388e3c", width=3)
    return img

def draw_salatalik(stage):
    # Draws a cucumber at the given growth stage
    img = Image.new("RGBA", (32, 32), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    if stage == 1:
        draw.ellipse([14, 18, 18, 22], fill="#8bc34a")  # Small cucumber
    elif stage == 2:
        draw.ellipse([14, 18, 18, 22], fill="#8bc34a")
        draw.line([16, 14, 16, 18], fill="#388e3c", width=2)
    elif stage == 3:
        draw.ellipse([10, 12, 22, 26], fill="#8bc34a")
    else:
        draw.ellipse([8, 8, 24, 28], fill="#8bc34a")
        draw.line([16, 4, 16, 8], fill="#388e3c", width=2)
    return img

def draw_misir(stage):
    # Draws a corn at the given growth stage
    img = Image.new("RGBA", (32, 32), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    if stage == 1:
        draw.ellipse([14, 18, 18, 22], fill="#ffd600")  # Small corn
    elif stage == 2:
        draw.ellipse([14, 18, 18, 22], fill="#ffd600")
        draw.line([16, 14, 16, 18], fill="#388e3c", width=2)
    elif stage == 3:
        draw.ellipse([12, 10, 20, 26], fill="#ffd600")
    else:
        draw.ellipse([10, 8, 22, 26], fill="#ffd600")
        draw.polygon([(10, 26), (16, 20), (22, 26)], fill="#388e3c")
    return img

def draw_bugday(stage):
    # Draws a wheat at the given growth stage
    img = Image.new("RGBA", (32, 32), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    if stage == 1:
        draw.ellipse([15, 19, 17, 21], fill="#fbc02d")  # Small wheat
    elif stage == 2:
        draw.ellipse([15, 19, 17, 21], fill="#fbc02d")
        draw.line([16, 15, 16, 19], fill="#a1887f", width=2)
    elif stage == 3:
        draw.rectangle([15, 10, 17, 22], fill="#fbc02d")
    else:
        draw.polygon([(16, 6), (18, 10), (16, 26), (14, 10)], fill="#fbc02d")
        draw.line([16, 2, 16, 6], fill="#a1887f", width=2)
    return img

def yield_function(x):
    """
    Parabolic yield function: yield = -((x - 50)**2) + 100
    x: water amount
    """
    return -((x - 50)**2) + 100

def yield_derivative(x):
    """
    Derivative of the yield function: d/dx [ -((x - 50)**2) + 100 ] = -2*(x - 50)
    """
    return -2 * (x - 50)

def find_optimal_water_amount(method="newton", bracket=(0, 100), x0=10):
    """
    Finds the water amount that gives maximum yield.
    method: 'bisect' or 'newton'
    bracket: (min, max) range (for bisection)
    x0: initial guess (for newton)
    """
    if method == "bisect":
        result = root_scalar(yield_derivative, method="bisect", bracket=bracket)
    else:
        result = root_scalar(yield_derivative, method="newton", x0=x0)
    if result.converged:
        optimum_x = result.root
        optimum_yield = yield_function(optimum_x)
        return optimum_x, optimum_yield
    else:
        return None, None

# Flask endpoint to get optimal water amount for maximum yield
app = Flask(__name__)

@app.route('/optimal_water', methods=['GET'])
def optimal_water():
    method = request.args.get('method', 'newton')  # Get method from query string
    optimum_x, optimum_yield = find_optimal_water_amount(method=method)
    if optimum_x is not None:
        return jsonify({
            'optimal_water': round(optimum_x, 2),  # Return rounded values
            'max_yield': round(optimum_yield, 2)
        })
    else:
        return jsonify({'error': 'Could not find optimal value.'}), 400

# Ensure output directory exists
img_dir = "static/img"
os.makedirs(img_dir, exist_ok=True)

# Generate and save images for each crop and stage
for crop, func in zip([
    "domates", "biber", "salatalik", "misir", "bugday"
], [draw_domates, draw_biber, draw_salatalik, draw_misir, draw_bugday]):
    for stage in range(1, 5):
        img = func(stage)  # Draw image for each stage
        img.save(f"{img_dir}/{crop}_{stage}.png")  # Save image
print("Simple crop-like placeholder images created.")

# Example usage:
if __name__ == "__main__":
    optimum_x, optimum_yield = find_optimal_water_amount()
    print(f"Optimum water amount: {optimum_x:.2f} L, Maximum yield: {optimum_yield:.2f}")
