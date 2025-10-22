import numpy as np

def bayesian_linear_regression(x, y, x_predict):
    """
    Performs Bayesian linear regression and returns predictions.
    Uses conjugate prior for simple implementation.
    """
    if len(x) < 2:
        return None
    
    # Convert to numpy arrays
    x = np.array(x, dtype=float)
    y = np.array(y, dtype=float)
    
    # Design matrix (add intercept)
    X = np.column_stack([np.ones(len(x)), x])
    
    # Prior parameters (weak prior)
    alpha_prior = 1e-6  # precision of prior
    beta = 1.0  # noise precision (assumed)
    
    # Posterior parameters
    S_inv = alpha_prior * np.eye(2) + beta * X.T @ X
    S = np.linalg.inv(S_inv)
    m = beta * S @ X.T @ y
    
    # Make predictions
    X_predict = np.column_stack([np.ones(len(x_predict)), x_predict])
    y_predict = X_predict @ m
    
    return y_predict


def moving_average(x, y, x_predict, window=3):
    """
    Simple moving average prediction.
    """
    if len(y) < window:
        return None
    
    # Calculate moving average of last 'window' points
    avg = np.mean(y[-window:])
    
    # Predict same value for all future points
    return np.full(len(x_predict), avg)


def exponential_smoothing(x, y, x_predict, alpha=0.3):
    """
    Exponential smoothing prediction.
    """
    if len(y) < 2:
        return None
    
    # Calculate exponential smoothing
    smoothed = y[0]
    for val in y[1:]:
        smoothed = alpha * val + (1 - alpha) * smoothed
    
    # Use last smoothed value as prediction
    return np.full(len(x_predict), smoothed)


def polynomial_regression(x, y, x_predict, degree=2):
    """
    Polynomial regression prediction.
    """
    if len(x) < degree + 1:
        return None
    
    # Fit polynomial
    coeffs = np.polyfit(x, y, degree)
    poly = np.poly1d(coeffs)
    
    # Make predictions
    return poly(x_predict)


# Dictionary mapping method names to functions
PREDICTION_METHODS = {
    "Bayesian Inference": lambda x, y, x_pred: bayesian_linear_regression(x, y, x_pred),
    "Moving Average": lambda x, y, x_pred: moving_average(x, y, x_pred, window=3),
    "Exponential Smoothing": lambda x, y, x_pred: exponential_smoothing(x, y, x_pred, alpha=0.3),
    "Polynomial Regression": lambda x, y, x_pred: polynomial_regression(x, y, x_pred, degree=2),
}