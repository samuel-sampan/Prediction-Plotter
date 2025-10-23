from taipy.gui import Gui
import numpy as np

# Analysis methods
analysis_methods = ["Bayesian Inference", "Moving Average", "Exponential Smoothing", "Polynomial Regression"]
selection = []

# Data storage
x_vals = []
y_vals = []
current_value = 0

# Chart data in Taipy format
chart_data = {"Entry Number": [], "Value": [], "Type": []}


# ---------- Prediction Functions ----------
def bayesian_linear_regression(x, y, x_predict):
    if len(x) < 2:
        return None
    x = np.array(x, dtype=float)
    y = np.array(y, dtype=float)
    X = np.column_stack([np.ones(len(x)), x])
    alpha_prior = 1e-6
    beta = 1.0
    S_inv = alpha_prior * np.eye(2) + beta * X.T @ X
    S = np.linalg.inv(S_inv)
    m = beta * S @ X.T @ y
    X_predict = np.column_stack([np.ones(len(x_predict)), x_predict])
    y_predict = X_predict @ m
    return y_predict


def moving_average(x, y, x_predict, window=3):
    if len(y) < window:
        window = len(y)
    avg = np.mean(y[-window:])
    return np.full(len(x_predict), avg)


def exponential_smoothing(x, y, x_predict, alpha=0.3):
    if len(y) < 2:
        return None
    smoothed = y[0]
    for val in y[1:]:
        smoothed = alpha * val + (1 - alpha) * smoothed
    return np.full(len(x_predict), smoothed)


def polynomial_regression(x, y, x_predict, degree=2):
    if len(x) < degree + 1:
        return None
    coeffs = np.polyfit(x, y, degree)
    poly = np.poly1d(coeffs)
    return poly(x_predict)


# ---------- Core Logic ----------
def update_chart(state):
    entry_numbers = state.x_vals.copy()
    values = state.y_vals.copy()
    types = ["User Input"] * len(entry_numbers)

    if len(state.x_vals) >= 2:
        last_x = state.x_vals[-1]
        x_predict = np.array([last_x + i for i in range(1, 11)])

        if "Bayesian Inference" in state.selection:
            predictions = bayesian_linear_regression(state.x_vals, state.y_vals, x_predict)
            if predictions is not None:
                entry_numbers.extend(x_predict.tolist())
                values.extend(predictions.tolist())
                types.extend(["Bayesian Inference"] * 10)

        if "Moving Average" in state.selection:
            predictions = moving_average(state.x_vals, state.y_vals, x_predict, window=3)
            if predictions is not None:
                entry_numbers.extend(x_predict.tolist())
                values.extend(predictions.tolist())
                types.extend(["Moving Average"] * 10)

        if "Exponential Smoothing" in state.selection:
            predictions = exponential_smoothing(state.x_vals, state.y_vals, x_predict, alpha=0.3)
            if predictions is not None:
                entry_numbers.extend(x_predict.tolist())
                values.extend(predictions.tolist())
                types.extend(["Exponential Smoothing"] * 10)

        if "Polynomial Regression" in state.selection:
            predictions = polynomial_regression(state.x_vals, state.y_vals, x_predict, degree=2)
            if predictions is not None:
                entry_numbers.extend(x_predict.tolist())
                values.extend(predictions.tolist())
                types.extend(["Polynomial Regression"] * 10)

    state.chart_data = {
        "Entry Number": entry_numbers,
        "Value": values,
        "Type": types
    }


def add_point(state):
    state.x_vals.append(len(state.x_vals) + 1)
    state.y_vals.append(state.current_value)
    update_chart(state)


def clear_data(state):
    """Clears all data for a fresh start."""
    state.x_vals = []
    state.y_vals = []
    state.chart_data = {"Entry Number": [], "Value": [], "Type": []}


def on_selection_change(state):
    update_chart(state)


# ---------- GUI Layout ----------
page = """
# Prediction Plotter

<|layout|columns=2 1 1|
**Enter a value:**  
<|{current_value}|number|>
<|Add Point|button|on_action=add_point|>
<|Clear Data|button|on_action=clear_data|class=clear-btn|>
|>

<|{chart_data}|chart|type=scatter|mode=lines+markers|x=Entry Number|y=Value|color=Type|height=500px|rebuild|color[User Input]=#FF0000|color[Bayesian Inference]=#FFA500|>

**Analysis Methods:**  
<|{selection}|selector|lov={analysis_methods}|multiple|on_change=on_selection_change|>
"""

# Run the app
import os
from taipy.gui import Gui

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    gui = Gui(page=page)
    gui.run(host="0.0.0.0", port=port, use_reloader=False)
