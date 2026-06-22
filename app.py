# This Flask app simulates agricultural irrigation optimization and plant growth.
# It provides endpoints for optimum/minimum values, growth calculation, growth rate, total growth, and crop comparison.

from flask import Flask, render_template, request, jsonify  # Import Flask modules
import os  # For file operations
import numpy as np  # For numerical calculations

app = Flask(__name__)

@app.route('/')
def index():
    # Render the main HTML page
    return render_template('index.html')

# Optimum values for each crop (temperature, water, fertilizer)
OPTIMUM_VALUES = {
    'tomato': {'temperature': 25, 'water': 6, 'fertilizer': 3},
    'pepper': {'temperature': 24, 'water': 5, 'fertilizer': 2},
    'cucumber': {'temperature': 22, 'water': 5, 'fertilizer': 2},
    'corn': {'temperature': 26, 'water': 7, 'fertilizer': 4},
    'wheat': {'temperature': 20, 'water': 4, 'fertilizer': 3}
}
# Minimum required water and fertilizer for each crop
MIN_VALUES = {
    'tomato': {'water': 3, 'fertilizer': 1},
    'pepper': {'water': 2, 'fertilizer': 1},
    'cucumber': {'water': 2, 'fertilizer': 1},
    'corn': {'water': 4, 'fertilizer': 2},
    'wheat': {'water': 2, 'fertilizer': 1}
}

def round_input(value):
    # Rounds user input to the nearest integer
    try:
        return round(float(value))
    except (ValueError, TypeError):
        return value

def calculate_growth(water, fertilizer, temperature, day):
    """
    Calculates plant growth for the n-th day using the formula:
    growth = (0.4*WATER + 0.3*FERTILIZER + 0.3*TEMP) * n
    """
    return (0.4 * water + 0.3 * fertilizer + 0.3 * temperature) * day

@app.route('/get_optimum', methods=['POST'])
def get_optimum():
    # Returns optimum values and comparison for the selected crop and user input
    data = request.json
    crop = data.get('crop')
    user_temp = round_input(data.get('temp'))
    user_water = round_input(data.get('amount'))
    user_fertilizer = round_input(data.get('fertilizer'))
    optimum = OPTIMUM_VALUES.get(crop, {})
    optimum_temp = optimum.get('temperature')
    optimum_water = optimum.get('water')
    optimum_fertilizer = optimum.get('fertilizer')
    temp_status = 'Ideal' if user_temp == optimum_temp else ('Low' if user_temp < optimum_temp else 'High')
    water_status = 'Ideal' if user_water == optimum_water else ('Low' if user_water < optimum_water else 'High')
    fertilizer_status = 'Ideal' if user_fertilizer == optimum_fertilizer else ('Low' if user_fertilizer < optimum_fertilizer else 'High')
    return jsonify({
        'optimum_temp': optimum_temp,
        'optimum_water': optimum_water,
        'optimum_fertilizer': optimum_fertilizer,
        'user_temp': user_temp,
        'user_water': user_water,
        'user_fertilizer': user_fertilizer,
        'temp_status': temp_status,
        'water_status': water_status,
        'fertilizer_status': fertilizer_status
    })

@app.route('/get_minimums', methods=['POST'])
def get_minimums():
    # Returns minimum required water and fertilizer for the selected crop
    data = request.json
    crop = data.get('crop')
    min_vals = MIN_VALUES.get(crop, {})
    return jsonify(min_vals)

@app.route('/growth_graph', methods=['POST'])
def growth_graph():
    # Interpolates plant height for 50 days using user-provided day/height data
    from scipy.interpolate import interp1d
    import numpy as np
    data = request.json
    days = data.get('days', [])
    heights = data.get('heights', [])
    method = data.get('method', 'linear')
    if not days or not heights or len(days) != len(heights):
        return jsonify({'error': 'Invalid data'}), 400
    days = np.array(days)
    heights = np.array(heights)
    x_new = np.arange(1, 51)
    if method == 'spline' and len(days) > 2:
        kind = 'cubic' if len(days) > 3 else 'linear'
        f = interp1d(days, heights, kind=kind, fill_value='extrapolate')
        y_new = f(x_new).tolist()
    else:
        f = interp1d(days, heights, kind='linear', fill_value='extrapolate')
        y_new = f(x_new).tolist()
    return jsonify({'days': x_new.tolist(), 'heights': y_new})

@app.route('/growth_graph_formula', methods=['POST'])
def growth_graph_formula():
    # Calculates plant height for 50 days using the main growth formula and user parameters
    data = request.json
    temp = float(data.get('temp', 0))
    water = float(data.get('amount', 0))
    fertilizer = float(data.get('fertilizer', 0))
    days = list(range(1, 51))
    heights = [(0.4 * water + 0.3 * fertilizer + 0.3 * temp) * n for n in days]
    return jsonify({'days': days, 'heights': heights})

@app.route('/growth_rate', methods=['POST'])
def growth_rate():
    # Calculates daily growth rate (difference between consecutive days)
    data = request.json
    heights = data.get('heights', [])
    if not heights or len(heights) < 2:
        return jsonify({'error': 'Not enough data'}), 400
    rates = [heights[i] - heights[i-1] for i in range(1, len(heights))]
    rates = [0] + rates
    return jsonify({'growth_rate': rates})

@app.route('/total_growth', methods=['POST'])
def total_growth():
    # Calculates the total growth (approximate area under the curve) for the first 30 days
    data = request.json
    heights = data.get('heights', [])
    if not heights or len(heights) < 2:
        return jsonify({'error': 'Not enough data'}), 400
    total = 0
    for i in range(1, min(31, len(heights))):
        total += (heights[i] + heights[i-1]) / 2
    return jsonify({'total_growth': total})

@app.route('/compare_crops', methods=['POST'])
def compare_crops():
    # Compares two crops under the same conditions: growth, rate, and total growth
    data = request.json
    crop1 = data.get('crop1')
    crop2 = data.get('crop2')
    temp = float(data.get('temp', 0))
    water = float(data.get('amount', 0))
    fertilizer = float(data.get('fertilizer', 0))
    days = list(range(1, 51))
    heights1 = [(0.4 * water + 0.3 * fertilizer + 0.3 * temp) * n for n in days]  # Crop 1 heights
    heights2 = [(0.4 * water + 0.3 * fertilizer + 0.3 * temp) * n for n in days]  # Crop 2 heights
    rates1 = [0] + [heights1[i] - heights1[i-1] for i in range(1, len(heights1))]  # Crop 1 rates
    rates2 = [0] + [heights2[i] - heights2[i-1] for i in range(1, len(heights2))]  # Crop 2 rates
    total1 = sum((heights1[i] + heights1[i-1]) / 2 for i in range(1, min(31, len(heights1))))  # Crop 1 total
    total2 = sum((heights2[i] + heights2[i-1]) / 2 for i in range(1, min(31, len(heights2))))  # Crop 2 total
    return jsonify({
        'crop1': crop1,
        'crop2': crop2,
        'heights1': heights1,
        'heights2': heights2,
        'rates1': rates1,
        'rates2': rates2,
        'total1': total1,
        'total2': total2
    })

# Solve a small linear system to find the effect of water and fertilizer on yield
# A: matrix of water and fertilizer values
# x: unknown effect coefficients
# b: observed yields

def solve_yield_system(water_list, fertilizer_list, yield_list):
    """
    Solves A*x = b for x, where:
    - A: n x 2 matrix (columns: water, fertilizer)
    - x: [water_effect, fertilizer_effect]
    - b: n x 1 vector (yield)
    Returns: [water_effect, fertilizer_effect]
    """
    A = np.column_stack((water_list, fertilizer_list))  # Build matrix A
    b = np.array(yield_list)  # Build vector b
    x = np.linalg.solve(A, b)  # Solve for x
    return x

# Example Flask endpoint to solve the system from user data
@app.route('/solve_yield_system', methods=['POST'])
def solve_yield_system_api():
    data = request.json
    water = data.get('water')  # list of water values
    fertilizer = data.get('fertilizer')  # list of fertilizer values
    yields = data.get('yield')  # list of observed yields
    if not (water and fertilizer and yields) or not (len(water) == len(fertilizer) == len(yields)):
        return jsonify({'error': 'Invalid input'}), 400
    try:
        coeffs = solve_yield_system(water, fertilizer, yields)
        return jsonify({'water_effect': coeffs[0], 'fertilizer_effect': coeffs[1]})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# --- Advanced Numerical Methods Examples (Backend Only) ---
# These are for demonstration/documentation and are NOT used in the web interface.

from scipy.integrate import odeint
from scipy.linalg import lu_factor, lu_solve
from scipy.optimize import root_scalar

# 1. ODE Solution Example: Simple plant growth model
def ode_growth_example():
    """
    Solves dG/dt = r*G*(1 - G/K) (logistic growth)
    Returns time points and solution array.
    """
    r = 0.2  # growth rate
    K = 100  # carrying capacity
    def dGdt(G, t):
        return r * G * (1 - G / K)
    G0 = 5  # initial growth
    t = np.linspace(0, 50, 100)
    G = odeint(dGdt, G0, t).flatten()
    return t, G

# 2. LU Decomposition Example
def lu_decomposition_example():
    """
    Solves Ax = b using LU decomposition (scipy.linalg.lu_factor/lu_solve)
    Returns x and the LU factors.
    """
    A = np.array([[3, 1, 2], [6, 3, 4], [3, 1, 5]], dtype=float)
    b = np.array([0, 1, 3], dtype=float)
    lu, piv = lu_factor(A)
    x = lu_solve((lu, piv), b)
    return x, lu, piv

# 3. Root Finding Comparison Example
def root_finding_comparison():
    """
    Compares bisection, Newton, and secant methods for f(x) = x^3 - x - 2
    Returns roots and number of iterations for each method.
    """
    def f(x):
        return x**3 - x - 2
    def fprime(x):
        return 3*x**2 - 1
    # Bisection
    bisect = root_scalar(f, bracket=[1, 2], method='bisect')
    # Newton
    newton = root_scalar(f, x0=1.5, fprime=fprime, method='newton')
    # Secant
    secant = root_scalar(f, x0=1, x1=2, method='secant')
    return {
        'bisection': {'root': bisect.root, 'iterations': bisect.iterations},
        'newton': {'root': newton.root, 'iterations': newton.iterations},
        'secant': {'root': secant.root, 'iterations': secant.iterations}
    }

# These functions are for backend demonstration/documentation only and are not called by the web app.
# You can test them in a Python shell or notebook for advanced numerical methods showcase.
# --- End of Advanced Numerical Methods Examples ---

if __name__ == '__main__':
    # Start the Flask development server
    app.run(debug=True)
