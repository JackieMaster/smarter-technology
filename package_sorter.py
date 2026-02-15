"""
Package Sorting System for Smarter Technology's Robotic Automation Factory

This module provides functionality to sort packages into appropriate stacks
based on their physical dimensions and mass.
"""

def sort(width, height, length, mass):
    """
    Sorts packages into appropriate dispatch stacks based on volume and mass.
    
    Args:
        width (float): Package width in centimeters
        height (float): Package height in centimeters
        length (float): Package length in centimeters
        mass (float): Package mass in kilograms
    
    Returns:
        str: Stack destination - "STANDARD", "SPECIAL", or "REJECTED"
    
    Classification Rules:
        - BULKY: volume >= 1,000,000 cm³ OR any dimension >= 150 cm
        - HEAVY: mass >= 20 kg
        - STANDARD: neither bulky nor heavy
        - SPECIAL: either bulky or heavy (but not both)
        - REJECTED: both bulky and heavy
    
    Examples:
        >>> sort(100, 100, 100, 15)
        'STANDARD'
        >>> sort(150, 50, 50, 15)
        'SPECIAL'
        >>> sort(200, 200, 200, 25)
        'REJECTED'
    """
    # Input validation
    if width <= 0 or height <= 0 or length <= 0 or mass <= 0:
        raise ValueError("All dimensions and mass must be positive values")
    
    # Check if package is bulky
    volume = width * height * length
    is_bulky = volume >= 1_000_000 or width >= 150 or height >= 150 or length >= 150
    
    # Check if package is heavy
    is_heavy = mass >= 20
    
    # Dispatch logic
    if is_bulky and is_heavy:
        return "REJECTED"
    elif is_bulky or is_heavy:
        return "SPECIAL"
    else:
        return "STANDARD"


if __name__ == "__main__":
    # Quick demonstration
    print("Package Sorting System Demo")
    print("=" * 50)
    
    test_cases = [
        (100, 100, 100, 15, "STANDARD"),
        (150, 100, 100, 15, "SPECIAL - bulky dimension"),
        (100, 100, 100, 25, "SPECIAL - heavy"),
        (200, 150, 100, 25, "REJECTED"),
    ]
    
    for width, height, length, mass, description in test_cases:
        result = sort(width, height, length, mass)
        print(f"{description}")
        print(f"  Dimensions: {width}x{height}x{length} cm, Mass: {mass} kg")
        print(f"  Result: {result}\n")
