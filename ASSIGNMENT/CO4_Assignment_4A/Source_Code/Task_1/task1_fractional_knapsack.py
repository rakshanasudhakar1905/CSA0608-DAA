"""
Task 1: Fractional Knapsack (Logistics Vehicle Loading)
Course: CSA06 Design and Analysis of Algorithms (CO4 - Assignment 4A)
"""

def load_vehicle(packages, capacity):
    """
    Maximizes total value loaded into a delivery vehicle allowing fractional packages.
    packages: list of tuples (id, weight, value)
    capacity: maximum vehicle weight capacity
    """
    if capacity <= 0 or not packages:
        return 0.0, []

    # Calculate value-to-weight density and sort descending
    enriched = []
    for pkg_id, weight, value in packages:
        if weight > 0:
            enriched.append((value / weight, pkg_id, weight, value))
    
    enriched.sort(key=lambda x: x[0], reverse=True)

    remaining_capacity = float(capacity)
    total_value = 0.0
    manifest = []

    for ratio, pkg_id, weight, value in enriched:
        if remaining_capacity <= 0:
            break
        if weight <= remaining_capacity:
            fraction = 1.0
            taken_weight = float(weight)
            taken_value = float(value)
        else:
            fraction = remaining_capacity / weight
            taken_weight = remaining_capacity
            taken_value = value * fraction

        total_value += taken_value
        remaining_capacity -= taken_weight
        manifest.append({
            "id": pkg_id,
            "fraction": round(fraction, 4),
            "weight_taken": round(taken_weight, 2),
            "value_gained": round(taken_value, 2)
        })

    return round(total_value, 2), manifest


if __name__ == "__main__":
    # Test Case 1: Standard Logistics Dataset
    sample_packages = [
        ("P1", 10, 60),   # Ratio: 6.0
        ("P2", 20, 100),  # Ratio: 5.0
        ("P3", 30, 120),  # Ratio: 4.0
        ("P4", 15, 45)    # Ratio: 3.0
    ]
    cap = 50
    max_val, loaded = load_vehicle(sample_packages, cap)
    print("=== Test Case 1: Standard Dataset (Capacity = 50) ===")
    print(f"Maximum Total Value: {max_val}")
    for item in loaded:
        print(f"  Package {item['id']}: {item['fraction']*100:.1f}% | Weight: {item['weight_taken']} | Value: {item['value_gained']}")

    # Test Case 2: Capacity exceeds total weight
    max_val2, loaded2 = load_vehicle(sample_packages, 100)
    print("\n=== Test Case 2: Surplus Capacity (Capacity = 100) ===")
    print(f"Maximum Total Value: {max_val2} (Items loaded: {len(loaded2)})")

    # Test Case 3: Zero Capacity Edge Case
    max_val3, loaded3 = load_vehicle(sample_packages, 0)
    print("\n=== Test Case 3: Zero Capacity (Capacity = 0) ===")
    print(f"Maximum Total Value: {max_val3} (Items loaded: {len(loaded3)})")
