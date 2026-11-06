import math


def power(base: float, exponent: float) -> float:
    """
    Calculate the power of a number.

    Args:
        base (float): The base number.
        exponent (float): The exponent to raise the base to.

    Returns:
        float: The result of base raised to the power of exponent.
    """
    return math.pow(base, exponent)


def square_root(x: float) -> float:
    """
    Calculate the square root of a number.

    Args:
        x (float): The number to calculate the square root of.

    Returns:
        float: The square root of x.

    Raises:
        ValueError: If x is negative.
    """
    if x < 0:
        raise ValueError("Cannot take square root of a negative number.")
    return math.sqrt(x)
