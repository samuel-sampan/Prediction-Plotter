import numpy as np
from database import save_entry


# Analysis methods

analysis_methods = ["Bayesian Inference", "Moving Average",
                    "Exponential Smoothing", "Polynomial Regression"]
selection = []
@@ -15,7 +17,13 @@
# Chart data in Taipy format
chart_data = {"Entry Number": [], "Value": [], "Type": []}

# Legal consent popup thingy
show_disclaimer = True  # Show at startup
user_accepted = False   # Track acceptance state


# Prediction Functions

def bayesian_linear_regression(x, y, x_predict):
    if len(x) < 2:
        return None
@@ -56,7 +64,8 @@ def polynomial_regression(x, y, x_predict, degree=2):
    return poly(x_predict)


#  Core Logic
# Core Logic

def update_chart(state):
    entry_numbers = state.x_vals.copy()
    values = state.y_vals.copy()
@@ -106,23 +115,18 @@ def update_chart(state):


def add_point(state):
    """Triggered when user clicks the button."""
    if not state.user_accepted:
        state.show_disclaimer = True
        return

    print(f"Button clicked! Current value: {state.current_value}")
    print(f"Before - x_vals: {state.x_vals}, y_vals: {state.y_vals}")
    
    state.x_vals.append(len(state.x_vals) + 1)
    state.y_vals.append(state.current_value)
    
    # Save to database (anonymous - no user ID)
    save_entry(len(state.x_vals), state.current_value)
    
    print(f"After - x_vals: {state.x_vals}, y_vals: {state.y_vals}")
    
    update_chart(state)


def clear_data(state):
    """Clears all data for a fresh start."""
    state.x_vals = []
    state.y_vals = []
    state.chart_data = {"Entry Number": [], "Value": [], "Type": []}
@@ -132,10 +136,29 @@ def on_selection_change(state):
    update_chart(state)


def accept_terms(state):
    state.show_disclaimer = False
    state.user_accepted = True


# GUI Layout

page = """
# Prediction Plotter

<|part|render={show_disclaimer}|
<|layout|columns=1|
### ⚠️ Disclaimer
This tool is provided for educational and experimental purposes only.  
By continuing, you acknowledge and agree that:
- All data entered may be **anonymized and stored** for research and model improvement.
- The predictions shown are **not guaranteed** and should not be interpreted as financial or factual forecasts.
- The creators are **not liable** for decisions made based on the tool’s output.

<|I Accept|button|on_action=accept_terms|class=accept-btn|>
|>
|>

<|layout|columns=2 1 1|
**Enter a value:**  
<|{current_value}|number|>
@@ -149,11 +172,10 @@ def on_selection_change(state):
<|{selection}|selector|lov={analysis_methods}|multiple|on_change=on_selection_change|>
"""

# Run the app

import os
from taipy.gui import Gui
# Run App

import os
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    gui = Gui(page=page)
